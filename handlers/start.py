from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import require_auth
from keyboards.menus import get_main_menu

@require_auth()
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    welcome_message = (
        f"👋 **Welcome, {user.first_name}!**\n\n"
        "I'm your Telegram Multi-Account Management Bot. "
        "I can help you manage multiple Telegram accounts and perform various operations.\n\n"
        "**Available Features:**\n"
        "• 📊 Account Management\n"
        "• 💬 Send Messages\n"
        "• 📢 Channel Operations\n"
        "• 👥 Group Management\n"
        "• 🤖 Bot Creation\n"
        "• 🚨 Reporting Tools\n"
        "• ➡️ Message Forwarding\n"
        "• 📋 Task Monitoring\n\n"
        "Use the menu below to get started or type /help for detailed instructions."
    )
    
    await update.message.reply_text(
        welcome_message,
        parse_mode="Markdown",
        reply_markup=get_main_menu(user.id)
    )


@require_auth()
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "📖 **Bot Help Guide**\n\n"
        "**Basic Commands:**\n"
        "• `/start` - Start the bot and show main menu\n"
        "• `/help` - Show this help message\n"
        "• `/accounts` - Manage Telegram accounts\n"
        "• `/send` - Send messages\n"
        "• `/channels` - Channel operations\n"
        "• `/groups` - Group management\n"
        "• `/createbot` - Create new bots\n"
        "• `/report` - Report users/channels\n"
        "• `/forward` - Forward messages\n"
        "• `/tasks` - View and manage tasks\n"
        "• `/health` - Check API health\n\n"
        "**Admin Commands (Super Admin Only):**\n"
        "• `/approve <user_id>` - Approve a user\n"
        "• `/revoke <user_id>` - Revoke user access\n"
        "• `/block <user_id>` - Block a user\n"
        "• `/users` - List all users\n"
        "• `/pending` - Show pending approvals\n"
        "• `/stats` - Show bot statistics\n"
        "• `/broadcast` - Broadcast message to all users\n\n"
        "**Account Management:**\n"
        "View the status of all your Telegram accounts, authorize new accounts, "
        "and reactivate inactive ones.\n\n"
        "**Sending Messages:**\n"
        "Send messages to users or channels using multiple accounts. "
        "You can select accounts manually or let the system choose automatically.\n\n"
        "**Channel Operations:**\n"
        "Create channels, join channels, view posts, and react to messages.\n\n"
        "**Reporting:**\n"
        "Report users or channels for various violations. Supports both quick reports "
        "and continuous reporting campaigns.\n\n"
        "**Task Management:**\n"
        "Monitor ongoing tasks like continuous reporting campaigns. "
        "View detailed statistics and stop tasks when needed.\n\n"
        "💡 **Tips:**\n"
        "• Use the keyboard menu for quick navigation\n"
        "• Most operations support both auto and manual account selection\n"
        "• Task dashboards auto-refresh every 30 seconds\n"
        "• You can cancel any multi-step operation by typing /cancel\n\n"
        "Need more help? Contact the administrator."
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


@require_auth()
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command"""
    # Clear any ongoing conversation state
    context.user_data.clear()
    
    await update.message.reply_text(
        "❌ Operation cancelled.\n\nUse the menu to start a new operation.",
        reply_markup=get_main_menu(update.effective_user.id)
    )
    
    return -1  # End conversation
