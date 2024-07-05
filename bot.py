# bot.py

import discord
import os
from discord.ext import commands
from discord import app_commands
from cryptography.fernet import Fernet

# Import the TextSubmission class
from text_submission import TextSubmission

# Import the TextSubmission and SubmissionRoleManager class
from role_manager import RoleManager
from role_manager import SubmissionRoleManager

def load_token(file_name='config.txt'):
    """Load the bot token from a configuration file."""
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith('TOKEN='):
                    return line.strip().split('=')[1]
    raise ValueError("Bot token not found in the config file.")

# Initialize the bot with a command prefix and intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize the TextSubmission instance
text_manager = TextSubmission()
role_manager = RoleManager()
submission_role_manager = SubmissionRoleManager()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Hybrid command for submit
@bot.hybrid_command(name='submit', description="Submit text with a category")
@app_commands.describe(category="Choose from 'safe', 'questionable', or 'nsfw'", text="The text to submit")
async def submit(ctx, category: str, *, text: str):
    if category.lower() not in ['safe', 'questionable', 'nsfw']:
        await ctx.send("Invalid category! Please choose from 'safe', 'questionable', or 'nsfw'.")
        return

    if submission_role_manager.can_submit(ctx.author.roles):
        user = f"{ctx.author.name}#{ctx.author.discriminator}"
        if text_manager.submit_text(user, category.lower(), text):
            await ctx.send(f'Text submitted by {user} in category {category}: "{text}"')
        else:
            await ctx.send(f'The prompt "{text}" already exists in the submissions.')
    else:
        await ctx.send("You do not have the required role to submit text.")

# Hybrid command for random
@bot.hybrid_command(name='random', description="Get a random submission, optionally filtered by category")
@app_commands.describe(category="Choose from 'safe', 'questionable', 'nsfw', or leave blank for all categories")
async def random_submission(ctx, category: str = None):
    if category and category.lower() not in ['safe', 'questionable', 'nsfw']:
        await ctx.send("Invalid category! Please choose from 'safe', 'questionable', 'nsfw', or leave it blank for all categories.")
        return
    
    submission = text_manager.get_random_submission(category.lower() if category else None)
    await ctx.send(f'Random submission: "{submission}"')

# Hybrid command for delete
@bot.hybrid_command(name='delete', description="Delete a user's submission")
@app_commands.describe(text="The text to delete")
async def delete_submission(ctx, *, text: str):
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    is_admin = role_manager.is_admin(ctx.author.roles)
    if text_manager.delete_text(user, text, admin=is_admin):
        await ctx.send(f'Text deleted: {text}')
    else:
        await ctx.send(f'No matching text found or insufficient permissions: {text}')

# Hybrid command for addrole
@bot.hybrid_command(name='addrole', description="Add a role that can delete any submission")
@commands.has_permissions(administrator=True)
@app_commands.describe(role="The role to add")
async def add_role(ctx, *, role: discord.Role):
    if role_manager.add_role(role.id):
        await ctx.send(f'Role {role.name} added to admin roles.')
    else:
        await ctx.send(f'Role {role.name} is already an admin role.')

# Hybrid command for removerole
@bot.hybrid_command(name='removerole', description="Remove a role that can delete any submission")
@commands.has_permissions(administrator=True)
@app_commands.describe(role="The role to remove")
async def remove_role(ctx, *, role: discord.Role):
    if role_manager.remove_role(role.id):
        await ctx.send(f'Role {role.name} removed from admin roles.')
    else:
        await ctx.send(f'Role {role.name} is not an admin role.')

# Hybrid command for addsubmitrole
@bot.hybrid_command(name='addsubmitrole', description="Add a role that can submit text")
@commands.has_permissions(administrator=True)
@app_commands.describe(role="The role to add")
async def add_submit_role(ctx, *, role: discord.Role):
    if submission_role_manager.add_role(role.id):
        await ctx.send(f'Role {role.name} added to submission roles.')
    else:
        await ctx.send(f'Role {role.name} is already a submission role.')

# Hybrid command for removesubmitrole
@bot.hybrid_command(name='removesubmitrole', description="Remove a role that can submit text")
@commands.has_permissions(administrator=True)
@app_commands.describe(role="The role to remove")
async def remove_submit_role(ctx, *, role: discord.Role):
    if submission_role_manager.remove_role(role.id):
        await ctx.send(f'Role "{role.name}" removed from submission roles.')
    else:
        await ctx.send(f'Role "{role.name}" is not a submission role.')

# Hybrid command for getsubmissions
@bot.hybrid_command(name='getsubmissions', description="Get all submissions as a downloadable .txt file")
@commands.cooldown(1, 180, commands.BucketType.user)
@app_commands.describe(category="Choose from 'safe', 'questionable', 'nsfw', or leave blank for all categories")
async def get_submissions(ctx, category: str = None):
    if category and category.lower() not in ['safe', 'questionable', 'nsfw']:
        await ctx.send("Invalid category! Please choose from 'safe', 'questionable', 'nsfw', or leave it blank for all categories.")
        return
    
    submissions = text_manager.get_all_submissions(category.lower() if category else None)
    file_path = f'submissions_output_{category or "all"}.txt'
    with open(file_path, 'w') as file:
        file.write(submissions)
    try:
        await ctx.author.send(file=discord.File(file_path))
        await ctx.send("The submissions have been sent to your DMs.")
    except discord.Forbidden:
        await ctx.send("I can't send you DMs. Please check your DM settings.")
    os.remove(file_path)

@get_submissions.error
async def get_submissions_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.")

# Hybrid command for info
@bot.hybrid_command(name='info', description="Display information about the bot")
async def info(ctx):
    help_message = (
        "Commands:\n"
        "/submit <category> <text> - Submit text in a category (safe, questionable, nsfw).\n"
        "/random [category] - Get a random submission, optionally filtered by category.\n"
        "/delete <text> - Delete your own submission. Admins can delete any submission.\n"
        "/addrole <role> - Add a role that can delete any submission. (Admin only)\n"
        "/removerole <role> - Remove a role that can delete any submission. (Admin only)\n"
        "/addsubmitrole <role> - Add a role that can submit texts. (Admin only)\n"
        "/removesubmitrole <role> - Remove a role that can submit texts. (Admin only)\n"
        "/getsubmissions [category] - Get all submissions in your DM, optionally filtered by category (3-minute cooldown).\n"
        "/info - Display this help message.\n"
        "/exit - Shut down the bot. (Bot owner only)"
    )
    await ctx.send(help_message)

# Hybrid command for exit
@bot.hybrid_command(name='exit', description="Shut down the bot (Bot owner only)")
@commands.is_owner()
async def exit_bot(ctx):
    await ctx.send("Exiting the bot.")
    await bot.close()

# Run the bot with your token
bot_token = load_token()
bot.run(bot_token)