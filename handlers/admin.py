from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import require_auth
from database import Database
from keyboards.menus import get_admin_menu
from config import STATUS_APPROVED, STATUS_PENDING, STATUS_BLOCKED

db = Database()

@require_auth(admin_only=True)
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command - show admin menu"""
    await update.message.reply_text(
        "⚙️ **Admin Panel**\n\nSelect an option:",
        parse_mode="Markdown",
        reply_markup=get_admin_menu()
    )


@require_auth(admin_only=True)
async def approve_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /approve <user_id> command"""
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "❌ **Usage:** `/approve <user_id>`\n\n"
            "Example: `/approve 123456789`",
            parse_mode="Markdown"
        )
        return
    
    try:
        target_user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Must be a number.")
        return
    
    # Approve the user
    if db.approve_user(target_user_id, update.effective_user.id):
        await update.message.reply_text(
            f"✅ User `{target_user_id}` has been approved!",
            parse_mode="Markdown"
        )
        
        # Notify the approved user
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="🎉 **Congratulations!**\n\n"
                     "Your access to the bot has been approved!\n"
                     "You can now use all features. Type /start to begin.",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Could not notify user {target_user_id}: {e}")
    else:
        await update.message.reply_text(
            f"❌ Failed to approve user `{target_user_id}`. "
            "User may not exist in the database.",
            parse_mode="Markdown"
        )


@require_auth(admin_only=True)
async def revoke_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /revoke <user_id> command"""
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "❌ **Usage:** `/revoke <user_id>`\n\n"
            "Example: `/revoke 123456789`",
            parse_mode="Markdown"
        )
        return
    
    try:
        target_user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Must be a number.")
        return
    
    if db.revoke_user(target_user_id):
        await update.message.reply_text(
            f"✅ Access revoked for user `{target_user_id}`",
            parse_mode="Markdown"
        )
        
        # Notify the user
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="⚠️ Your access to this bot has been revoked by the administrator.",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Could not notify user {target_user_id}: {e}")
    else:
        await update.message.reply_text(
            f"❌ Failed to revoke access for user `{target_user_id}`",
            parse_mode="Markdown"
        )


@require_auth(admin_only=True)
async def block_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /block <user_id> command"""
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "❌ **Usage:** `/block <user_id>`\n\n"
            "Example: `/block 123456789`",
            parse_mode="Markdown"
        )
        return
    
    try:
        target_user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Must be a number.")
        return
    
    if db.block_user(target_user_id):
        await update.message.reply_text(
            f"🚫 User `{target_user_id}` has been blocked permanently.",
            parse_mode="Markdown"
        )
        
        # Notify the user
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="🚫 You have been blocked from using this bot.",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Could not notify user {target_user_id}: {e}")
    else:
        await update.message.reply_text(
            f"❌ Failed to block user `{target_user_id}`",
            parse_mode="Markdown"
        )


@require_auth(admin_only=True)
async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /users command - list all users"""
    users = db.get_all_users()
    
    if not users:
        await update.message.reply_text("No users found in the database.")
        return
    
    # Group users by status
    approved = [u for u in users if u['status'] == STATUS_APPROVED]
    pending = [u for u in users if u['status'] == STATUS_PENDING]
    blocked = [u for u in users if u['status'] == STATUS_BLOCKED]
    
    message = "👥 **All Users**\n\n"
    
    if approved:
        message += "✅ **Approved Users:**\n"
        for user in approved:
            username = f"@{user['username']}" if user['username'] else "No username"
            message += f"• `{user['user_id']}` - {user['first_name']} ({username})\n"
        message += "\n"
    
    if pending:
        message += "⏳ **Pending Users:**\n"
        for user in pending:
            username = f"@{user['username']}" if user['username'] else "No username"
            message += f"• `{user['user_id']}` - {user['first_name']} ({username})\n"
        message += "\n"
    
    if blocked:
        message += "🚫 **Blocked Users:**\n"
        for user in blocked:
            username = f"@{user['username']}" if user['username'] else "No username"
            message += f"• `{user['user_id']}` - {user['first_name']} ({username})\n"
    
    await update.message.reply_text(message, parse_mode="Markdown")


@require_auth(admin_only=True)
async def pending_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pending command - show pending approvals"""
    pending_users = db.get_pending_users()
    
    if not pending_users:
        await update.message.reply_text("✅ No pending approval requests.")
        return
    
    message = "⏳ **Pending Approval Requests:**\n\n"
    
    for user in pending_users:
        username = f"@{user['username']}" if user['username'] else "No username"
        message += (
            f"━━━━━━━━━━\n"
            f"**User:** {user['first_name']} ({username})\n"
            f"**ID:** `{user['user_id']}`\n"
            f"**Requested:** {user['added_at']}\n"
            f"**Action:** `/approve {user['user_id']}`\n"
        )
    
    await update.message.reply_text(message, parse_mode="Markdown")


@require_auth(admin_only=True)
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command - show bot statistics"""
    stats = db.get_user_stats()
    
    message = (
        "📊 **Bot Statistics**\n\n"
        f"**Total Users:** {stats['total']}\n"
        f"✅ Approved: {stats['approved']}\n"
        f"⏳ Pending: {stats['pending']}\n"
        f"🚫 Blocked: {stats['blocked']}\n"
    )
    
    await update.message.reply_text(message, parse_mode="Markdown")
