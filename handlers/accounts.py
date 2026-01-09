from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from utils.decorators import require_auth
from api_client import TelegramAPIClient
from config import PHONE, CODE, PASSWORD
from keyboards.menus import get_accounts_menu, get_cancel_keyboard

api_client = TelegramAPIClient()

@require_auth()
async def accounts_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show status of all accounts"""
    query = update.callback_query
    if query:
        await query.answer()
    
    msg = await (query.message.edit_text if query else update.message.reply_text)(
        "⏳ Fetching account status...",
        parse_mode="Markdown"
    )
    
    try:
        result = api_client.get_accounts_status()
        accounts = result.get('accounts', [])
        
        if not accounts:
            text = "📊 **Account Status**\n\n❌ No accounts found."
        else:
            text = "📊 **Account Status**\n\n"
            
            active = [a for a in accounts if a.get('is_active')]
            inactive = [a for a in accounts if not a.get('is_active')]
            
            if active:
                text += "🟢 **Active Accounts:**\n"
                for acc in active:
                    phone = acc.get('phone', 'Unknown')
                    name = acc.get('name', 'No name')
                    text += f"• `{phone}` - {name}\n"
                text += "\n"
            
            if inactive:
                text += "🔴 **Inactive Accounts:**\n"
                for acc in inactive:
                    phone = acc.get('phone', 'Unknown')
                    name = acc.get('name', 'No name')
                    text += f"• `{phone}` - {name}\n"
                text += "\n"
            
            text += f"━━━━━━━━━━\n"
            text += f"**Total:** {len(accounts)} | **Active:** {len(active)} | **Inactive:** {len(inactive)}"
        
        # Add refresh button
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="accounts_status")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu_accounts")]
        ]
        
        await msg.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error fetching account status:**\n\n`{str(e)}`",
            parse_mode="Markdown",
            reply_markup=get_accounts_menu()
        )


@require_auth()
async def start_authorize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start account authorization process"""
    query = update.callback_query
    if query:
        await query.answer()
        msg = query.message
    else:
        msg = update.message
    
    await msg.reply_text(
        "🔐 **Authorize New Account**\n\n"
        "Please enter the phone number in international format.\n\n"
        "**Example:** +1234567890\n\n"
        "Type /cancel to abort.",
        parse_mode="Markdown",
        reply_markup=get_cancel_keyboard()
    )
    
    return PHONE


@require_auth()
async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive phone number and request code"""
    phone = update.message.text.strip()
    
    # Validate phone format
    if not phone.startswith('+'):
        await update.message.reply_text(
            "❌ Phone number must start with '+' and include country code.\n\n"
            "**Example:** +1234567890\n\n"
            "Please try again or /cancel:",
            parse_mode="Markdown"
        )
        return PHONE
    
    context.user_data['phone'] = phone
    
    # Send authorization request
    msg = await update.message.reply_text("⏳ Sending authorization code...")
    
    try:
        result = api_client.authorize_account(phone=phone)
        
        if result.get('code_sent'):
            await msg.edit_text(
                "✅ **Authorization code sent!**\n\n"
                f"A code has been sent to `{phone}`\n\n"
                "Please enter the verification code:",
                parse_mode="Markdown"
            )
            return CODE
        else:
            await msg.edit_text(
                f"❌ Failed to send code:\n\n`{result.get('message', 'Unknown error')}`",
                parse_mode="Markdown"
            )
            return ConversationHandler.END
    
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:**\n\n`{str(e)}`",
            parse_mode="Markdown"
        )
        return ConversationHandler.END


@require_auth()
async def receive_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive verification code"""
    code = update.message.text.strip()
    phone = context.user_data.get('phone')
    
    msg = await update.message.reply_text("⏳ Verifying code...")
    
    try:
        result = api_client.authorize_account(phone=phone, code=code)
        
        if result.get('success'):
            await msg.edit_text(
                "✅ **Account authorized successfully!**\n\n"
                f"Phone: `{phone}`\n"
                f"Name: {result.get('name', 'N/A')}",
                parse_mode="Markdown"
            )
            context.user_data.clear()
            return ConversationHandler.END
        
        elif result.get('requires_password'):
            await msg.edit_text(
                "🔒 **Two-Factor Authentication Required**\n\n"
                "Please enter your 2FA password:",
                parse_mode="Markdown"
            )
            return PASSWORD
        
        else:
            await msg.edit_text(
                f"❌ Authorization failed:\n\n`{result.get('message', 'Unknown error')}`",
                parse_mode="Markdown"
            )
            return ConversationHandler.END
    
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:**\n\n`{str(e)}`",
            parse_mode="Markdown"
        )
        return ConversationHandler.END


@require_auth()
async def receive_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive 2FA password"""
    password = update.message.text.strip()
    phone = context.user_data.get('phone')
    
    # Delete the message containing the password for security
    await update.message.delete()
    
    msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="⏳ Verifying 2FA password..."
    )
    
    try:
        result = api_client.authorize_account(phone=phone, password=password)
        
        if result.get('success'):
            await msg.edit_text(
                "✅ **Account authorized successfully!**\n\n"
                f"Phone: `{phone}`\n"
                f"Name: {result.get('name', 'N/A')}",
                parse_mode="Markdown"
            )
        else:
            await msg.edit_text(
                f"❌ Authorization failed:\n\n`{result.get('message', 'Incorrect password')}`",
                parse_mode="Markdown"
            )
        
        context.user_data.clear()
        return ConversationHandler.END
    
    except Exception as e:
        await msg.edit_text(
            f"❌ **Error:**\n\n`{str(e)}`",
            parse_mode="Markdown"
        )
        context.user_data.clear()
        return ConversationHandler.END


@require_auth()
async def reactivate_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reactivate inactive accounts"""
    query = update.callback_query
    if query:
        await query.answer()
        msg = query.message
    else:
        msg = update.message
    
    # First get account status to find inactive accounts
    loading = await msg.reply_text("⏳ Fetching inactive accounts...")
    
    try:
        result = api_client.get_accounts_status()
        accounts = result.get('accounts', [])
        inactive = [a for a in accounts if not a.get('is_active')]
        
        if not inactive:
            await loading.edit_text(
                "✅ No inactive accounts found!\n\n"
                "All accounts are currently active.",
                parse_mode="Markdown"
            )
            return
        
        # Get phone numbers of inactive accounts
        phones = [a.get('phone') for a in inactive]
        
        await loading.edit_text(
            f"🔄 **Reactivating {len(phones)} inactive accounts...**\n\n"
            "This may take a moment...",
            parse_mode="Markdown"
        )
        
        # Reactivate
        reactivate_result = api_client.reactivate_accounts(phones=phones)
        
        success_count = reactivate_result.get('success_count', 0)
        failed_count = reactivate_result.get('failed_count', 0)
        
        text = "🔄 **Reactivation Complete**\n\n"
        text += f"✅ Success: {success_count}\n"
        text += f"❌ Failed: {failed_count}\n"
        
        if reactivate_result.get('details'):
            text += "\n━━━━━━━━━━\n**Details:**\n"
            for detail in reactivate_result['details'][:5]:  # Show first 5
                status = "✅" if detail.get('success') else "❌"
                text += f"{status} `{detail.get('phone')}`\n"
        
        await loading.edit_text(text, parse_mode="Markdown")
    
    except Exception as e:
        await loading.edit_text(
            f"❌ **Error:**\n\n`{str(e)}`",
            parse_mode="Markdown"
        )
