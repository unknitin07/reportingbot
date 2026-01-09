from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from utils.decorators import require_auth
from api_client import TelegramAPIClient
from config import SELECT_ACCOUNTS, TARGET, MESSAGE, CONFIRM
from keyboards.menus import get_account_selection_keyboard, get_confirmation_keyboard, get_cancel_keyboard

api_client = TelegramAPIClient()

@require_auth()
async def send_message_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start send message flow"""
    await update.message.reply_text(
        "💬 **Send Message**\n\n"
        "Choose how to select accounts:",
        parse_mode="Markdown",
        reply_markup=get_account_selection_keyboard("send")
    )
    return SELECT_ACCOUNTS


@require_auth()
async def account_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle account selection mode"""
    query = update.callback_query
    await query.answer()

    data = query.data

    if "auto" in data:
        context.user_data['account_mode'] = 'auto'
        await query.message.edit_text(
            "✅ **Auto Mode Selected**\n\n"
            "How many accounts do you want to use?\n\n"
            "Enter a number (e.g., `1`, `5`, `10`) or type `all` to use all available accounts:",
            parse_mode="Markdown"
        )
        return SELECT_ACCOUNTS

    elif "manual" in data:
        context.user_data['account_mode'] = 'manual'
        await query.message.edit_text(
            "✋ **Manual Mode Selected**\n\n"
            "Enter phone numbers (comma-separated):\n\n"
            "**Example:**\n"
            "`+1234567890, +0987654321`",
            parse_mode="Markdown"
        )
        return SELECT_ACCOUNTS


@require_auth()
async def receive_manual_phones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive manually selected phones or account count"""
    text = update.message.text.strip()

    # Auto mode - expecting account count
    if context.user_data.get('account_mode') == 'auto':
        if text.lower() == 'all':
            context.user_data['account_count'] = None  # API will use all
            await update.message.reply_text(
                "✅ Will use all available accounts\n\n"
                "Now, enter the target (username, phone, or channel):\n\n"
                "**Examples:**\n"
                "• `@username`\n"
                "• `+1234567890`\n"
                "• `@channelname`",
                parse_mode="Markdown"
            )
        else:
            try:
                count = int(text)
                if count < 1:
                    await update.message.reply_text(
                        "❌ Count must be at least 1. Please try again:",
                        reply_markup=get_cancel_keyboard()
                    )
                    return SELECT_ACCOUNTS

                context.user_data['account_count'] = count
                await update.message.reply_text(
                    f"✅ Will use {count} account(s)\n\n"
                    "Now, enter the target (username, phone, or channel):\n\n"
                    "**Examples:**\n"
                    "• `@username`\n"
                    "• `+1234567890`\n"
                    "• `@channelname`",
                    parse_mode="Markdown"
                )
            except ValueError:
                await update.message.reply_text(
                    "❌ Invalid number. Enter a number (e.g., `5`) or type `all`:",
                    reply_markup=get_cancel_keyboard()
                )
                return SELECT_ACCOUNTS

        return TARGET

    # Manual mode - expecting phone numbers
    elif context.user_data.get('account_mode') == 'manual':
        phones = [p.strip() for p in text.replace(',', '\n').split('\n') if p.strip()]

        if not phones:
            await update.message.reply_text(
                "❌ No valid phone numbers provided. Please try again:",
                reply_markup=get_cancel_keyboard()
            )
            return SELECT_ACCOUNTS

        context.user_data['phones'] = phones

        await update.message.reply_text(
            f"✅ Selected {len(phones)} account(s)\n\n"
            "Now, enter the target (username, phone, or channel):\n\n"
            "**Examples:**\n"
            "• `@username`\n"
            "• `+1234567890`\n"
            "• `@channelname`",
            parse_mode="Markdown"
        )
        return TARGET

    return TARGET


@require_auth()
async def receive_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive target"""
    target = update.message.text.strip()

    if not target:
        await update.message.reply_text(
            "❌ Target cannot be empty. Please try again:",
            reply_markup=get_cancel_keyboard()
        )
        return TARGET

    context.user_data['target'] = target

    await update.message.reply_text(
        f"✅ Target: `{target}`\n\n"
        "Now, enter your message:\n\n"
        "💡 You can write multiple lines.",
        parse_mode="Markdown",
        reply_markup=get_cancel_keyboard()
    )
    return MESSAGE


@require_auth()
async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive message content"""
    message_text = update.message.text.strip()

    if not message_text:
        await update.message.reply_text(
            "❌ Message cannot be empty. Please try again:",
            reply_markup=get_cancel_keyboard()
        )
        return MESSAGE

    context.user_data['message'] = message_text

    # Show preview
    target = context.user_data.get('target')
    mode = context.user_data.get('account_mode')
    phones = context.user_data.get('phones', [])
    account_count = context.user_data.get('account_count')

    preview = (
        "📋 **Message Preview**\n\n"
        f"**Target:** `{target}`\n"
        f"**Mode:** {mode.title()}\n"
    )

    if mode == 'manual':
        preview += f"**Accounts:** {len(phones)}\n"
    else:
        if account_count:
            preview += f"**Accounts:** {account_count}\n"
        else:
            preview += f"**Accounts:** All available\n"

    preview += f"\n**Message:**\n{message_text[:200]}"
    if len(message_text) > 200:
        preview += "..."

    preview += "\n\n━━━━━━━━━━\nReady to send?"

    await update.message.reply_text(
        preview,
        parse_mode="Markdown",
        reply_markup=get_confirmation_keyboard("send_confirm", "send_cancel")
    )
    return CONFIRM


@require_auth()
async def confirm_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm and send message"""
    query = update.callback_query
    await query.answer()

    if query.data == "send_cancel":
        await query.message.edit_text("❌ Message sending cancelled.")
        context.user_data.clear()
        return ConversationHandler.END

    # Get data
    target = context.user_data.get('target')
    message = context.user_data.get('message')
    mode = context.user_data.get('account_mode')
    phones = context.user_data.get('phones')
    account_count = context.user_data.get('account_count')

    # Show progress
    msg = await query.message.edit_text(
        "⏳ **Sending messages...**\n\n"
        "Please wait, this may take a moment.",
        parse_mode="Markdown"
    )

    try:
        # Call API
        if mode == 'auto':
            result = api_client.send_message(
                target=target,
                message=message,
                account_count=account_count
            )
        else:
            result = api_client.send_message(
                target=target,
                message=message,
                phones=phones
            )

        # Parse results
        success_count = result.get('success_count', 0)
        failed_count = result.get('failed_count', 0)
        details = result.get('details', [])

        # Format response
        response = "📬 **Message Sending Complete**\n\n"
        response += f"✅ Success: {success_count}\n"
        response += f"❌ Failed: {failed_count}\n"

        if details:
            response += "\n━━━━━━━━━━\n**Details:**\n"
            for detail in details[:5]:
                status = "✅" if detail.get('success') else "❌"
                phone = detail.get('phone', 'Unknown')
                response += f"{status} `{phone}`"
                if not detail.get('success'):
                    response += f" - {detail.get('error', 'Unknown error')}"
                response += "\n"

            if len(details) > 5:
                response += f"\n... and {len(details) - 5} more"

        await msg.edit_text(response, parse_mode="Markdown")

    except Exception as e:
        await msg.edit_text(
            f"❌ **Error sending messages:**\n\n`{str(e)}`",
            parse_mode="Markdown"
        )

    context.user_data.clear()
    return ConversationHandler.END


@require_auth()
async def cancel_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel send message flow"""
    await update.message.reply_text("❌ Message sending cancelled.")
    context.user_data.clear()
    return ConversationHandler.END
