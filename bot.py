import discord
import random
import os
from discord.ext import commands
from cryptography.fernet import Fernet

class TextSubmission:
    def __init__(self, file_name='submissions.txt', key_file='secret.key'):
        """Initialize the submission system with a file name and encryption key."""
        self.file_name = file_name
        self.key_file = key_file
        self.load_key()
        self.load_submissions()

    def load_key(self):
        """Load or generate an encryption key."""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as file:
                self.key = file.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(self.key)
        self.cipher = Fernet(self.key)

    def encrypt(self, text):
        """Encrypt a string using Fernet."""
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, text):
        """Decrypt a string using Fernet."""
        return self.cipher.decrypt(text.encode()).decode()

    def escape_newlines(self, text):
        """Escape newlines in the text."""
        return text.replace('\n', '\\n')

    def unescape_newlines(self, text):
        """Unescape newlines in the text."""
        return text.replace('\\n', '\n')

    def load_submissions(self):
        """Load submissions from the file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.submissions = [line.strip().split('::', 2) for line in file]
                self.submissions = [(self.decrypt(user), category, self.unescape_newlines(text)) for user, category, text in self.submissions]
        else:
            self.submissions = []

    def save_submissions(self):
        """Save submissions to the file."""
        with open(self.file_name, 'w') as file:
            for submission in self.submissions:
                encrypted_user = self.encrypt(submission[0])
                escaped_text = self.escape_newlines(submission[2])
                file.write(f"{encrypted_user}::{submission[1]}::{escaped_text}\n")

    def submit_text(self, user, category, text):
        """Add a new text submission with a category and save to file if it doesn't already exist."""
        if text not in (submission[2] for submission in self.submissions):
            submission = (user, category, text)
            self.submissions.append(submission)
            self.save_submissions()
            return True
        return False

    def delete_text(self, user, text, admin=False):
        """Delete a text submission and save to file."""
        submission = [(u, c, t) for u, c, t in self.submissions if t == text and (admin or u == user)]
        if submission:
            self.submissions = [s for s in self.submissions if s not in submission]
            self.save_submissions()
            return True
        return False

    def get_random_submission(self, category=None):
        """Return a random text submission from the list, optionally filtered by category."""
        submissions = [s for s in self.submissions if category is None or s[1] == category]
        if submissions:
            return random.choice(submissions)[2]
        else:
            return "No submissions available."

    def get_all_submissions(self, category=None):
        """Return all text submissions from the list, optionally filtered by category."""
        submissions = [s for s in self.submissions if category is None or s[1] == category]
        if submissions:
            separator = "\n----------------------\n"
            return separator.join(submission[2] for submission in submissions)
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
                self.roles = [int(line.strip()) for line in file]
        else:
            self.roles = []

    def save_roles(self):
        """Save roles to the file."""
        with open(self.file_name, 'w') as file:
            for role in self.roles:
                file.write(f"{role}\n")

    def add_role(self, role_id):
        """Add a new role and save to file."""
        if role_id not in self.roles:
            self.roles.append(role_id)
            self.save_roles()
            return True
        return False

    def remove_role(self, role_id):
        """Remove a role and save to file."""
        if role_id in self.roles:
            self.roles.remove(role_id)
            self.save_roles()
            return True
        return False

    def is_admin(self, user_roles):
        """Check if any of the user's roles are in the admin roles list."""
        return any(role.id in self.roles for role in user_roles)

class SubmissionRoleManager:
    def __init__(self, file_name='submission_roles.txt'):
        """Initialize the submission role manager with a file name."""
        self.file_name = file_name
        self.load_roles()

    def load_roles(self):
        """Load roles from the file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.roles = [int(line.strip()) for line in file]
        else:
            self.roles = []

    def save_roles(self):
        """Save roles to the file."""
        with open(self.file_name, 'w') as file:
            for role in self.roles:
                file.write(f"{role}\n")

    def add_role(self, role_id):
        """Add a new role and save to file."""
        if role_id not in self.roles:
            self.roles.append(role_id)
            self.save_roles()
            return True
        return False

    def remove_role(self, role_id):
        """Remove a role and save to file."""
        if role_id in self.roles:
            self.roles.remove(role_id)
            self.save_roles()
            return True
        return False

    def can_submit(self, user_roles):
        """Check if any of the user's roles are in the submission roles list."""
        return any(role.id in self.roles for role in user_roles)

# Initialize the bot with a command prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)

# Initialize the TextSubmission instance
text_manager = TextSubmission()
role_manager = RoleManager()
submission_role_manager = SubmissionRoleManager()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='submit')
async def submit(ctx, category: str, *, text: str):
    """Command to submit text with a category."""
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


@bot.command(name='random')
async def random_submission(ctx, category: str = None):
    """Command to get a random submission, optionally filtered by category."""
    if category and category.lower() not in ['safe', 'questionable', 'nsfw']:
        await ctx.send("Invalid category! Please choose from 'safe', 'questionable', 'nsfw', or leave it blank for all categories.")
        return
    
    submission = text_manager.get_random_submission(category.lower() if category else None)
    await ctx.send(f'Random submission: "{submission}"')

@bot.command(name='delete')
async def delete_submission(ctx, *, text: str):
    """Command to delete a user's submission."""
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    is_admin = role_manager.is_admin(ctx.author.roles)
    if text_manager.delete_text(user, text, admin=is_admin):
        await ctx.send(f'Text deleted: {text}')
    else:
        await ctx.send(f'No matching text found or insufficient permissions: {text}')

@bot.command(name='addrole')
@commands.has_permissions(administrator=True)
async def add_role(ctx, *, role: discord.Role):
    """Command to add a role that can delete any submission."""
    if role_manager.add_role(role.id):
        await ctx.send(f'Role {role.name} added to admin roles.')
    else:
        await ctx.send(f'Role {role.name} is already an admin role.')

@bot.command(name='removerole')
@commands.has_permissions(administrator=True)
async def remove_role(ctx, *, role: discord.Role):
    """Command to remove a role that can delete any submission."""
    if role_manager.remove_role(role.id):
        await ctx.send(f'Role {role.name} removed from admin roles.')
    else:
        await ctx.send(f'Role {role.name} is not an admin role.')

@bot.command(name='addsubmitrole')
@commands.has_permissions(administrator=True)
async def add_submit_role(ctx, *, role: discord.Role):
    """Command to add a role that can submit text."""
    if submission_role_manager.add_role(role.id):
        await ctx.send(f'Role {role.name} added to submission roles.')
    else:
        await ctx.send(f'Role {role.name} is already a submission role.')

@bot.command(name='removesubmitrole')
@commands.has_permissions(administrator=True)
async def remove_submit_role(ctx, *, role: discord.Role):
    """Command to remove a role that can submit text."""
    if submission_role_manager.remove_role(role.id):
        await ctx.send(f'Role "{role.name}" removed from submission roles.')
    else:
        await ctx.send(f'Role "{role.name}" is not a submission role.')

@bot.command(name='getsubmissions')
@commands.cooldown(1, 180, commands.BucketType.user)  # 3-minute cooldown per user
async def get_submissions(ctx, category: str = None):
    """Command to get all submissions, optionally filtered by category, as a downloadable .txt file."""
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
    """Handle errors for the getsubmissions command."""
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.")

@bot.command(name='info')
async def info(ctx):
    """Command to display information about the bot."""
    help_message = (
        "Commands:\n"
        "!submit <category> <text> - Submit text in a category (safe, questionable, nsfw).\n"
        "!random [category] - Get a random submission, optionally filtered by category.\n"
        "!delete <text> - Delete your own submission. Admins can delete any submission.\n"
        "!addrole <role> - Add a role that can delete any submission. (Admin only)\n"
        "!removerole <role> - Remove a role that can delete any submission. (Admin only)\n"
        "!addsubmitrole <role> - Add a role that can submit texts. (Admin only)\n"
        "!removesubmitrole <role> - Remove a role that can submit texts. (Admin only)\n"
        "!getsubmissions [category] - Get all submissions in your DM, optionally filtered by category (3-minute cooldown).\n"
        "!info - Display this help message.\n"
        "!exit - Shut down the bot. (Bot owner only)"
    )
    await ctx.send(help_message)

@bot.command(name='exit')
@commands.is_owner()
async def exit_bot(ctx):
    """Command to exit the bot."""
    await ctx.send("Exiting the bot.")
    await bot.logout()

# Run the bot with your token
bot_token = load_token()
bot.run(bot_token)