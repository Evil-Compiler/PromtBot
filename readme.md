# Discord Text Submission Bot
This Discord bot allows users to submit text messages, which are stored and can be retrieved at random. 
Users can also delete their submissions, and administrators can delete any submission or manage roles that can perform deletion.

# Prerequisites
Python 3 installed on your system. 
>(Tested on `python 3.12.3`)

discord.py library installed. You can install it using pip:
`pip install discord.py`

cryptography library installed for encryption of user data. You can install it using pip:
`pip install cryptography`

# Installation and Setup
1. Clone or download the project repository to your local machine.

2. Ensure Python and the required libraries are installed.

3. Create a Discord bot and obtain its token. You can follow the [official Discord developer documentation](https://discord.com/developers/docs/intro) for detailed instructions.

4. Create a `config.txt` file in the project directory and add your bot token in the following format:`TOKEN=YOUR_DISCORD_BOT_TOKEN`

5. Run the bot script using Python:
`python bot.py`

# Usage
Once the bot is running and added to your Discord server, users can submit text messages using the !submit command followed by their message.

Users can retrieve a random submission using the !random command.

Users can delete their submissions using the !delete command followed by the text to delete.

Administrators can manage roles that can delete any submission using the !addrole and !removerole commands.

Administrators can delete any submission using the !delete command with appropriate permissions.

The !getsubmissions command allows users to retrieve all submissions. There is a 3-minute cooldown for this command per user.

# Running the Bot 24/7
There are 2 Options

## For Linux
### Setup
1. Open the `run_bot.sh` in a texteditor of youre choice

2. Replace `/path/to/your/bot` with the actual path to the directory where your bot.py script is located.

3. save the `run_bot.sh` file

4. Enter the following command to make the script executable: `chmod +x run_bot.sh`

5. Run

### Running the Script in the Background
To ensure the script runs in the background and continues running even if you close the terminal, you can use nohup or screen.

#### Using nohup:

`nohup ./run_bot.sh &`

#### Using screen:

1. Start a new screen session:
`screen -S mybot`

2. Run the script inside the screen session:
`./run_bot.sh`

3. Detach from the screen session by pressing Ctrl+A followed by D.

    To reattach to the screen session later, use:
`screen -r mybot`

By using this bash script and running it with nohup or screen, you can ensure that your Discord bot stays running 24/7 and automatically restarts if it crashes.

## For Windows
### Setup
1. Open the `run_bot.sh` in a texteditor of youre choice

2. Replace `C:\path\to\your\bot` with the actual path to the directory where your bot.py script is located.

3. save the `run_bot.bat` file

4. you can run the script by double-clicking `run_bot.bat` or by running it from the Command Prompt:
`run_bot.bat`

### Running the Script in the Background
todo