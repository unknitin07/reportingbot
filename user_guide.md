# Telegram Multi-Account Bot - User Guide

Complete guide to using all features of the Telegram Multi-Account Management Bot.

## Table of Contents
- [Getting Started](#getting-started)
- [Account Management](#account-management)
- [Sending Messages](#sending-messages)
- [Channel Operations](#channel-operations)
- [Group Management](#group-management)
- [Bot Creation](#bot-creation)
- [Reporting](#reporting)
- [Message Forwarding](#message-forwarding)
- [Task Management](#task-management)
- [Admin Features](#admin-features)

---

## Getting Started

### First Time Use

1. **Start the bot**: Send `/start` to your bot
2. **Authorization**: 
   - If you're the super admin (ID: 5813016547), you'll be automatically approved
   - If you're another user, you'll need to wait for admin approval

### Main Menu

After starting the bot, you'll see a keyboard menu with these options:

```
📊 Accounts  | 💬 Messages
📢 Channels  | 👥 Groups
🤖 Bots      | 🚨 Reports
➡️ Forward   | 📋 Tasks
⚕️ Health    | ⚙️ Admin (admin only)
```

---

## Account Management

Access via: **📊 Accounts** button or `/accounts` command

### View Account Status

Shows all your Telegram accounts with their current status.

**What you'll see:**
- 🟢 Active accounts (ready to use)
- 🔴 Inactive accounts (need reactivation)
- Account phone numbers and names
- Total statistics

**How to use:**
1. Click **📊 Accounts**
2. Click **📊 View Status**
3. Click **🔄 Refresh** to update the status

### Authorize New Account

Add a new Telegram account to your bot.

**Step-by-step:**
1. Click **📊 Accounts** → **🔐 Authorize Account**
2. Enter phone number in international format: `+1234567890`
3. Wait for verification code on your Telegram app
4. Enter the verification code
5. If you have 2FA enabled, enter your password
6. Done! Account is now active

**Important:**
- Phone must start with `+` and include country code
- You'll receive the code in your Telegram app
- The bot will ask for 2FA password only if you have it enabled

### Reactivate Inactive Accounts

Reactivate accounts that have become inactive.

**How to use:**
1. Click **📊 Accounts** → **🔄 Reactivate Accounts**
2. The bot will automatically find all inactive accounts
3. Confirm to reactivate them all
4. View the results

---

## Sending Messages

Access via: **💬 Messages** button or `/send` command

Send messages to users or channels using your accounts.

### Quick Send

**Step-by-step:**
1. Type `/send`
2. Choose account selection:
   - **🤖 Auto Select**: Bot chooses accounts automatically
   - **✋ Manual Select**: You specify which accounts to use
3. If manual, enter phone numbers (comma-separated):
   ```
   +1234567890, +0987654321
   ```
4. Enter target (username, phone, or channel):
   ```
   @username
   or
   +1234567890
   or
   @channelname
   ```
5. Type your message (can be multiline):
   ```
   Hello! This is a test message.
   
   It can have multiple lines.
   ```
6. Review and confirm
7. Watch the progress in real-time

**Examples:**

*Send to a user:*
```
Target: @johndoe
Message: Hi John! Hope you're doing well.
```

*Send to a channel:*
```
Target: @mychannel
Message: New update available! Check it out.
```

---

## Channel Operations

Access via: **📢 Channels** button or `/channels` command

### Create Channels

Create new Telegram channels using your accounts.

**Step-by-step:**
1. Click **📢 Channels** → **➕ Create Channel**
2. Enter channel title:
   ```
   My Awesome Channel
   ```
3. Enter channel description:
   ```
   This channel is about technology and innovation.
   ```
4. Choose privacy:
   - **Public**: Anyone can find and join
   - **Private**: Invite-only
5. Confirm and create

### Join Channels

Join existing channels with multiple accounts.

**Step-by-step:**
1. Click **📢 Channels** → **🔗 Join Channels**
2. Enter channel links (one per line or comma-separated):
   ```
   @channel1
   @channel2
   https://t.me/channel3
   ```
3. Choose accounts (auto or manual)
4. Confirm and join
5. View results

### View Channel Posts

View recent posts from a channel.

**Step-by-step:**
1. Click **📢 Channels** → **👁️ View Posts**
2. Enter channel username:
   ```
   @newsChannel
   ```
3. Enter number of posts to view (e.g., `10`)
4. Choose accounts
5. View the posts

### React to Posts

Add reactions to channel messages.

**Step-by-step:**
1. Click **📢 Channels** → **❤️ React to Posts**
2. Enter channel username
3. Enter message IDs (comma-separated):
   ```
   123, 124, 125
   ```
4. Choose emoji:
   - Select from emoji picker: 👍 ❤️ 🔥 👏 😂 😮 😢 🤔 💯 🎉 ⚡
   - Or enter custom emoji
5. Choose accounts
6. Confirm and react

---

## Group Management

Access via: **👥 Groups** button or `/groups` command

### Create Groups

Create new Telegram groups.

**Step-by-step:**
1. Click **👥 Groups** → **➕ Create Group**
2. Enter group title:
   ```
   Tech Enthusiasts
   ```
3. Enter group description:
   ```
   A group for discussing technology
   ```
4. Choose accounts
5. Confirm and create

---

## Bot Creation

Access via: **🤖 Bots** button or `/createbot` command

Create new Telegram bots through BotFather.

**Step-by-step:**
1. Type `/createbot`
2. Enter bot name:
   ```
   My Helper Bot
   ```
3. Enter bot username (must end with 'bot'):
   ```
   myhelper_bot
   ```
4. Choose accounts
5. Confirm
6. **Copy the bot token** (important!)
   - Token will be shown in monospace format
   - Save it securely
   - You'll need it to run the bot

**Important:**
- Bot username must end with 'bot'
- Username must be unique across Telegram
- Keep the bot token private and secure

---

## Reporting

Access via: **🚨 Reports** button or `/report` command

Report users or channels to Telegram for violations.

### Quick Report

One-time report for immediate action.

**Step-by-step:**
1. Click **🚨 Reports** → **⚡ Quick Report**
2. Enter targets (one per line):
   ```
   @spammer1
   @spammer2
   https://t.me/spam_channel
   ```
3. Select reason:
   - 🔞 Pornography
   - ⚠️ Violence
   - 👶 Child Abuse
   - 🚫 Spam
   - 💊 Illegal Drugs
   - © Copyright
   - 📝 Other
4. Choose accounts
5. Confirm and send
6. View results

### Continuous Reporting Campaign

Automated reporting at regular intervals.

**Step-by-step:**
1. Click **🚨 Reports** → **🔄 Continuous Campaign**
2. Enter targets (one per line)
3. Select reason
4. Choose accounts
5. Set interval in seconds (e.g., `300` for 5 minutes)
6. Optionally set start time (format: `YYYY-MM-DD HH:MM`)
7. Review configuration
8. Confirm to start

**Monitoring:**
- Campaign runs automatically at specified intervals
- View progress in **📋 Tasks** menu
- Dashboard auto-refreshes every 30 seconds
- Click **🛑 Stop** to end the campaign

---

## Message Forwarding

Access via: **➡️ Forward** button or `/forward` command

Forward messages from one channel to others.

**Step-by-step:**
1. Type `/forward`
2. Enter source channel:
   ```
   @source_channel
   ```
3. Enter destination channels (one per line):
   ```
   @dest_channel1
   @dest_channel2
   @dest_channel3
   ```
4. Enter message IDs to forward (comma-separated):
   ```
   100, 101, 102, 103
   ```
5. Choose accounts
6. Confirm and forward
7. View results

**Tips:**
- You can forward multiple messages at once
- Message IDs can be seen in the channel
- Accounts must be members of both source and destination channels

---

## Task Management

Access via: **📋 Tasks** button or `/tasks` command

Monitor and manage ongoing tasks like continuous reporting campaigns.

### View All Tasks

**What you'll see:**
- Task ID and type
- Status (running, completed, failed)
- Progress statistics
- Start time and duration
- Next execution time (for recurring tasks)

**How to use:**
1. Click **📋 Tasks**
2. View list of all tasks
3. Click on a task to see details

### Monitor a Task

**Dashboard features:**
- Real-time statistics
- Auto-refresh every 30 seconds
- Success/failure counts
- Accounts being used
- Actions performed

**Controls:**
- **🔄 Refresh**: Manual refresh
- **🛑 Stop**: Stop the task immediately
- **🔙 Back to Tasks**: Return to task list

### Stop a Task

**How to stop:**
1. Go to **📋 Tasks**
2. Click on the running task
3. Click **🛑 Stop**
4. Confirm
5. Task will stop and release accounts

---

## Admin Features

Access via: **⚙️ Admin** button (Super Admin Only)

Only user with ID `5813016547` has access to these features.

### Approve Users

Grant bot access to new users.

**Method 1: Via notification**
- When a new user tries to access the bot, you'll receive a notification
- Click the `/approve <user_id>` link in the notification

**Method 2: Manual command**
```
/approve 123456789
```

**Result:**
- User gets approved immediately
- User receives a notification
- User can now use all bot features

### Revoke Access

Remove bot access from a user.

```
/revoke 123456789
```

**Result:**
- User loses access to bot
- User receives a notification
- User can request access again later

### Block Users

Permanently block a user from accessing the bot.

```
/block 123456789
```

**Result:**
- User is permanently blocked
- User receives a notification
- User cannot use bot even if approved again

### View All Users

See all users with their status.

```
/users
```

**Shows:**
- ✅ Approved users
- ⏳ Pending users (waiting for approval)
- 🚫 Blocked users
- User IDs, usernames, and names

### Pending Approvals

View users waiting for approval.

```
/pending
```

**Shows:**
- User details
- When they requested access
- Quick approve link for each user

### Bot Statistics

View bot usage statistics.

```
/stats
```

**Shows:**
- Total users
- Approved users count
- Pending users count
- Blocked users count

---

## Tips & Best Practices

### General Tips

1. **Use /cancel anytime** to abort an operation
2. **Check /health** regularly to ensure API is working
3. **Monitor tasks** for continuous operations
4. **Save important information** like bot tokens immediately

### Account Management

1. **Authorize accounts gradually** to avoid rate limits
2. **Reactivate accounts** before starting large operations
3. **Keep track** of which phones are used for what purpose

### Sending Messages

1. **Test with one account first** before using all accounts
2. **Use auto-select** unless you have specific requirements
3. **Keep messages concise** for better delivery rates

### Reporting

1. **Use appropriate reasons** for reports to be effective
2. **Don't spam reports** - use reasonable intervals
3. **Monitor continuous campaigns** and stop when goals are met
4. **Use multiple accounts** for better impact

### Task Management

1. **Check tasks regularly** to ensure they're running smoothly
2. **Stop tasks** when no longer needed to free up accounts
3. **Note task IDs** for important operations

---

## Common Issues & Solutions

### "Access Denied"
- **Cause**: You're not approved yet
- **Solution**: Wait for admin approval or contact admin with your user ID

### "API Connection Error"
- **Cause**: API server is down or unreachable
- **Solution**: Contact admin to check API server

### "Account Inactive"
- **Cause**: Account session expired
- **Solution**: Use reactivate accounts feature

### "Operation Failed"
- **Cause**: Various reasons (rate limit, permissions, etc.)
- **Solution**: Check error message, wait a bit, try again

### "Invalid Format"
- **Cause**: Input doesn't match expected format
- **Solution**: Follow examples in bot messages

---

## Getting Help

If you need help:

1. **Check this guide** for detailed instructions
2. **Read error messages** carefully
3. **Try /help command** for quick reference
4. **Contact the bot administrator** if issue persists

---

## Command Reference

### Basic Commands
- `/start` - Start the bot
- `/help` - Show help message
- `/cancel` - Cancel current operation
- `/accounts` - Account management
- `/send` - Send messages
- `/channels` - Channel operations
- `/groups` - Group management
- `/createbot` - Create bots
- `/report` - Reporting tools
- `/forward` - Forward messages
- `/tasks` - Task management
- `/health` - Check API health

### Admin Commands (Super Admin Only)
- `/admin` - Admin panel
- `/approve <user_id>` - Approve user
- `/revoke <user_id>` - Revoke access
- `/block <user_id>` - Block user
- `/users` - List all users
- `/pending` - Pending approvals
- `/stats` - Bot statistics

---

**Happy automating! 🚀**
