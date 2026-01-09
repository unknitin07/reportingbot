#!/usr/bin/env python3
"""
Telegram Multi-Account Management Bot
Main entry point for the bot application
"""

import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

from config import TELEGRAM_BOT_TOKEN, LOG_LEVEL, LOG_FILE
from database import Database
from api_client import TelegramAPIClient

# Import handlers
from handlers.start import start_command, help_command, cancel_command
from handlers.admin import (
    admin_command, approve_user_command, revoke_user_command,
    block_user_command, users_command, pending_command, stats_command
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL),
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database()
api_client = TelegramAPIClient()


async def error_handler(update: Update, context):
    """Handle errors"""
    logger.error(f"Exception while handling an update: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred while processing your request. "
            "Please try again or contact the administrator."
        )


async def callback_query_handler(update: Update, context):
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Handle menu navigation
    if data == "menu_main":
        from keyboards.menus import get_main_menu
        await query.message.edit_text(
            "📋 **Main Menu**\n\nSelect an option:",
            parse_mode="Markdown",
            reply_markup=get_main_menu(update.effective_user.id)
        )
    
    elif data == "cancel":
        await query.message.edit_text("❌ Operation cancelled.")
        context.user_data.clear()
        return -1
    
    # Add more callback handlers here as needed
    # This is a basic structure - full implementation would have handlers
    # for all the menu options


async def message_handler(update: Update, context):
    """Handle text messages from main menu"""
    text = update.message.text
    user_id = update.effective_user.id
    
    from keyboards.menus import (
        get_accounts_menu, get_channels_menu, get_groups_menu,
        get_reports_menu, get_admin_menu
    )
    
    if text == "📊 Accounts":
        await update.message.reply_text(
            "📊 **Account Management**\n\nSelect an option:",
            parse_mode="Markdown",
            reply_markup=get_accounts_menu()
        )
    
    elif text == "💬 Messages":
        await update.message.reply_text(
            "💬 **Send Messages**\n\n"
            "Use /send to send messages to users or channels.",
            parse_mode="Markdown"
        )
    
    elif text == "📢 Channels":
        await update.message.reply_text(
            "📢 **Channel Operations**\n\nSelect an option:",
            parse_mode="Markdown",
            reply_markup=get_channels_menu()
        )
    
    elif text == "👥 Groups":
        await update.message.reply_text(
            "👥 **Group Management**\n\nSelect an option:",
            parse_mode="Markdown",
            reply_markup=get_groups_menu()
        )
    
    elif text == "🤖 Bots":
        await update.message.reply_text(
            "🤖 **Bot Creation**\n\n"
            "Use /createbot to create new Telegram bots.",
            parse_mode="Markdown"
        )
    
    elif text == "🚨 Reports":
        await update.message.reply_text(
            "🚨 **Reporting Tools**\n\nSelect an option:",
            parse_mode="Markdown",
            reply_markup=get_reports_menu()
        )
    
    elif text == "➡️ Forward":
        await update.message.reply_text(
            "➡️ **Message Forwarding**\n\n"
            "Use /forward to forward messages between channels.",
            parse_mode="Markdown"
        )
    
    elif text == "📋 Tasks":
        await update.message.reply_text(
            "📋 **Task Management**\n\n"
            "Use /tasks to view and manage running tasks.",
            parse_mode="Markdown"
        )
    
    elif text == "⚕️ Health":
        try:
            health = api_client.get_health()
            status_emoji = "🟢" if health.get('status') == 'healthy' else "🔴"
            
            await update.message.reply_text(
                f"⚕️ **API Health Status**\n\n"
                f"Status: {status_emoji} {health.get('status', 'unknown').upper()}\n"
                f"Active Accounts: {health.get('active_accounts', 0)}\n"
                f"Total Accounts: {health.get('total_accounts', 0)}\n"
                f"Running Tasks: {health.get('running_tasks', 0)}",
                parse_mode="Markdown"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Failed to fetch health status:\n`{str(e)}`",
                parse_mode="Markdown"
            )
    
    elif text == "⚙️ Admin":
        from config import SUPER_ADMIN_ID
        if user_id == SUPER_ADMIN_ID:
            await update.message.reply_text(
                "⚙️ **Admin Panel**\n\nSelect an option:",
                parse_mode="Markdown",
                reply_markup=get_admin_menu()
            )
        else:
            await update.message.reply_text("❌ Admin access required.")


async def post_init(application):
    """Run after bot initialization"""
    logger.info("Bot initialized successfully")
    
    # Test API connection
    try:
        health = api_client.ping()
        logger.info(f"API connection successful: {health}")
    except Exception as e:
        logger.error(f"Failed to connect to API: {e}")
        logger.error("Bot will continue running but API features may not work")


def main():
    """Main function to run the bot"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables")
        sys.exit(1)
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    # Admin commands
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("approve", approve_user_command))
    application.add_handler(CommandHandler("revoke", revoke_user_command))
    application.add_handler(CommandHandler("block", block_user_command))
    application.add_handler(CommandHandler("users", users_command))
    application.add_handler(CommandHandler("pending", pending_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    
    # Message handler for menu buttons
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
