# Quick Start Guide

Get your Telegram bot up and running in 5 minutes!

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Create Configuration File

Create a `.env` file:

```bash
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
API_BASE_URL=http://127.0.0.1:8000
SUPER_ADMIN_ID=5813016547
LOG_LEVEL=INFO
DATABASE_PATH=bot_database.db
```

## Step 3: Create Required Directories

```bash
mkdir -p handlers keyboards utils
touch handlers/__init__.py
touch keyboards/__init__.py
touch utils/__init__.py
```

## Step 4: Initialize Database

```bash
python init_db.py
```

## Step 5: Start the Bot

```bash
python bot.py
```

## Step 6: Test the Bot

1. Open Telegram
2. Search for your bot by username
3. Send `/start` command
4. You should see the welcome message and main menu!

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### "Token invalid" errors
- Get a new token from @BotFather
- Make sure token is correctly pasted in `.env` file
- No spaces before or after the token

### "Can't connect to API" errors
- Make sure the API server is running: `curl http://127.0.0.1:8000/ping`
- Check the API_BASE_URL in your `.env` file

### Bot doesn't respond
- Check logs: `tail -f bot.log`
- Make sure bot is running: `ps aux | grep bot.py`
- Restart the bot: Kill the process and run `python bot.py` again

## Next Steps

- Read the full README.md for detailed documentation
- Add more users with `/approve <user_id>`
- Configure accounts with `/accounts`
- Try sending messages with `/send`

## Getting Help

Check the logs for errors:
```bash
tail -f bot.log
```

View database contents:
```bash
sqlite3 bot_database.db "SELECT * FROM users;"
```

## Production Deployment

For production use, consider:
- Using systemd service (see telegram-bot.service file)
- Setting up log rotation
- Regular database backups
- Monitoring with health checks

---

🎉 **Congratulations!** Your bot is now ready to use.
