from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config import SUPER_ADMIN_ID, STATUS_BLOCKED
from database import Database
import time

db = Database()

# Rate limiting dictionary
_last_command_time = {}

def require_auth(admin_only=False):
    """
    Decorator to check if user is authorized to use the bot.
    
    Args:
        admin_only: If True, only super admin can execute this command
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            user_id = user.id
            
            # Add user to database if not exists
            db.add_user(
                user_id=user_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            # Check if user is blocked
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT status FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0] == STATUS_BLOCKED:
                await update.message.reply_text(
                    "🚫 You have been blocked from using this bot."
                )
                return
            
            # Check if user is approved
            if not db.is_user_approved(user_id):
                await update.message.reply_text(
                    "❌ **Access Denied**\n\n"
                    "You don't have permission to use this bot.\n"
                    "Your user ID has been forwarded to the admin for approval.\n\n"
                    f"Your ID: `{user_id}`",
                    parse_mode="Markdown"
                )
                
                # Notify super admin about new user
                try:
                    await context.bot.send_message(
                        chat_id=SUPER_ADMIN_ID,
                        text=f"🔔 **New user requesting access:**\n\n"
                             f"User ID: `{user_id}`\n"
                             f"Username: @{user.username or 'N/A'}\n"
                             f"Name: {user.full_name}\n\n"
                             f"Use `/approve {user_id}` to grant access",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print(f"Failed to notify admin: {e}")
                
                return
            
            # Check admin permission if required
            if admin_only and user_id != SUPER_ADMIN_ID:
                await update.message.reply_text(
                    "❌ **Admin Access Required**\n\n"
                    "This command can only be used by the bot administrator.",
                    parse_mode="Markdown"
                )
                return
            
            # Rate limiting (2 second cooldown)
            current_time = time.time()
            if user_id in _last_command_time:
                time_diff = current_time - _last_command_time[user_id]
                if time_diff < 2:
                    await update.message.reply_text(
                        "⏳ Please wait a moment before sending another command."
                    )
                    return
            
            _last_command_time[user_id] = current_time
            
            # User is authorized, proceed with the command
            return await func(update, context)
        
        return wrapper
    return decorator


def log_operation(operation_name: str):
    """
    Decorator to log operations to database.
    
    Args:
        operation_name: Name of the operation being performed
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            success = False
            params = {}
            
            try:
                result = await func(update, context, *args, **kwargs)
                success = True
                return result
            except Exception as e:
                success = False
                raise e
            finally:
                # Log the operation
                db.log_operation(
                    user_id=user_id,
                    operation=operation_name,
                    params=params,
                    success=success
                )
        
        return wrapper
    return decorator
