# Discord Text Submission Bot
This Discord bot allows users to submit text messages, which are stored and can be retrieved at random. Users can also delete their submissions, and administrators can delete any submission or manage roles that can perform deletion.

## Prerequisites
Python 3 installed on your system. 
>(Tested on `python 3.12.3`)

discord.py library installed. You can install it using pip:
`pip install discord.py`

cryptography library installed for encryption of user data. You can install it using pip:
`pip install cryptography`

## Installation and Setup
1. Clone or download the project repository to your local machine.

2. Ensure Python and the required libraries are installed.

3. Create a Discord bot and obtain its token. You can follow the official Discord developer documentation for detailed instructions.

4. Create a `config.txt` file in the project directory and add your bot token in the following format:`TOKEN=YOUR_DISCORD_BOT_TOKEN`

5. Run the bot script using Python:
`python bot.py`

## Usage
Once the bot is running and added to your Discord server, users can submit text messages using the !submit command followed by their message.

Users can retrieve a random submission using the !random command.

Users can delete their submissions using the !delete command followed by the text to delete.

Administrators can manage roles that can delete any submission using the !addrole and !removerole commands.

Administrators can delete any submission using the !delete command with appropriate permissions.

The !getsubmissions command allows users to retrieve all submissions. There is a 3-minute cooldown for this command per user.