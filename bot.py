import discord
import random
import os
from discord.ext import commands

class TextSubmission:
    def __init__(self, file_name='submissions.txt'):
        """Initialize the submission system with a file name."""
        self.file_name = file_name
        self.load_submissions()

    def load_submissions(self):
        """Load submissions from the file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.submissions = [line.strip().split('::', 1) for line in file]
        else:
            self.submissions = []

    def save_submissions(self):
        """Save submissions to the file."""
        with open(self.file_name, 'w') as file:
            for submission in self.submissions:
                file.write(f"{submission[0]}::{submission[1]}\n")

    def submit_text(self, user, text):
        """Add a new text submission and save to file."""
        submission = (user, text)
        self.submissions.append(submission)
        self.save_submissions()

    def delete_text(self, user, text, admin=False):
        """Delete a text submission and save to file."""
        submission = (user, text)
        if admin:
            # Admin deletion - remove any matching text
            matching_submissions = [s for s in self.submissions if text in s[1]]
            if matching_submissions:
                for match in matching_submissions:
                    self.submissions.remove(match)
                self.save_submissions()
                return True
        else:
            # User deletion - remove only if the user matches
            if submission in self.submissions:
                self.submissions.remove(submission)
                self.save_submissions()
                return True
        return False

    def get_random_submission(self):
        """Return a random text submission from the list."""
        if self.submissions:
            return random.choice(self.submissions)[1]
        else:
            return "No submissions available."

    def get_all_submissions(self):
        """Return all text submissions from the list, without usernames."""
        if self.submissions:
            return '\n'.join(submission[1] for submission in self.submissions)
        else:
            return "No submissions available."       

def load_token(file_name='config.txt'):
    """Load the bot token from a configuration file."""
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith('TOKEN='):
                    return line.strip().split('=')[1]
    raise ValueError("Bot token not found in the config file.")

class RoleManager:
    def __init__(self, file_name='admin_roles.txt'):
        """Initialize the role manager with a file name."""
        self.file_name = file_name
        self.load_roles()

    def load_roles(self):
        """Load roles from the file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.roles = [line.strip() for line in file]
        else:
            self.roles = ['Admin', 'Moderator']  # Default roles

    def save_roles(self):
        """Save roles to the file."""
        with open(self.file_name, 'w') as file:
            for role in self.roles:
                file.write(f"{role}\n")

    def add_role(self, role):
        """Add a new role and save to file."""
        if role not in self.roles:
            self.roles.append(role)
            self.save_roles()
            return True
        return False

    def remove_role(self, role):
        """Remove a role and save to file."""
        if role in self.roles:
            self.roles.remove(role)
            self.save_roles()
            return True
        return False

    def is_admin(self, user_roles):
        """Check if any of the user's roles are in the admin roles list."""
        return any(role.name in self.roles for role in user_roles)


# Initialize the bot with a command prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)

# Initialize the TextSubmission instance
text_manager = TextSubmission()
role_manager = RoleManager()

# Define the roles that can delete any submission
ADMIN_ROLES = ['Admin', 'Moderator']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='submit')
async def submit(ctx, *, text: str):
    """Command to submit text."""
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    text_manager.submit_text(user, text)
    await ctx.send(f'Text submitted by {user}: "{text}"')

@bot.command(name='random')
async def random_submission(ctx):
    """Command to get a random submission."""
    submission = text_manager.get_random_submission()
    await ctx.send(f'Random submission: "{submission}"')

@bot.command(name='delete')
async def delete_submission(ctx, *, text: str):
    """Command to delete a user's submission."""
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    is_admin = role_manager.is_admin(ctx.author.roles)
    if text_manager.delete_text(user, text, admin=is_admin):
        await ctx.send(f'Text deleted: "{text}"')
    else:
        await ctx.send(f'No matching text found or insufficient permissions: "{text}"')

@bot.command(name='addrole')
@commands.has_permissions(administrator=True)
async def add_role(ctx, *, role_name: str):
    """Command to add a role that can delete any submission."""
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        if role_manager.add_role(role_name):
            await ctx.send(f'Role "{role_name}" added to admin roles.')
        else:
            await ctx.send(f'Role "{role_name}" is already an admin role.')
    else:
        await ctx.send(f'Role "{role_name}" does not exist on this server.')

@bot.command(name='removerole')
@commands.has_permissions(administrator=True)
async def remove_role(ctx, *, role_name: str):
    """Command to remove a role that can delete any submission."""
    if role_manager.remove_role(role_name):
        await ctx.send(f'Role "{role_name}" removed from admin roles.')
    else:
        await ctx.send(f'Role "{role_name}" is not an admin role.')

@bot.command(name='getsubmissions')
async def get_submissions(ctx):
    """Command to get all submissions, sent as a DM to the user."""
    user = ctx.author
    submissions = text_manager.get_all_submissions()
    try:
        await user.send(f'All submissions:\n{submissions}')
        await ctx.send("The submissions have been sent to your DMs.")
    except discord.Forbidden:
        await ctx.send("I can't send you DMs. Please check your DM settings.")

@bot.command(name='exit')
@commands.is_owner()
async def exit_bot(ctx):
    """Command to exit the bot."""
    await ctx.send("Exiting the bot.")
    await bot.logout()

# Run the bot with your token
bot_token = load_token()
bot.run(bot_token)