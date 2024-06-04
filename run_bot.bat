@echo off
setlocal

:: This is the path to your bot's directory
set BOT_DIR=C:\path\to\your\bot

:: This is the path to your bot's main script
set BOT_SCRIPT=bot.py

:: Navigate to the bot directory
cd /d "%BOT_DIR%"

:loop
echo Starting bot...
python "%BOT_SCRIPT%"

:: If the bot crashes, wait for 5 seconds before restarting
echo Bot crashed with exit code %errorlevel%. Restarting in 5 seconds...
timeout /t 5 /nobreak

:: Go back to the start of the loop
goto loop