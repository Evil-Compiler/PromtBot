#!/bin/bash

# This is the path to your bot's directory
BOT_DIR="/path/to/your/bot"

# This is the path to your bot's main script
BOT_SCRIPT="bot.py"

# Navigate to the bot directory
cd "$BOT_DIR" || exit

# Function to start the bot
start_bot() {
    echo "Starting bot..."
    python3 "$BOT_SCRIPT"
}

# Loop to keep the bot running
while true; do
    start_bot
    echo "Bot crashed with exit code $?. Restarting in 5 seconds..."
    sleep 5
done