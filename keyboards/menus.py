from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPER_ADMIN_ID

def get_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    """Get main menu keyboard based on user permissions"""
    keyboard = [
        ["📊 Accounts", "💬 Messages"],
        ["📢 Channels", "👥 Groups"],
        ["🤖 Bots", "🚨 Reports"],
        ["➡️ Forward", "📋 Tasks"],
        ["⚕️ Health"]
    ]
    
    # Add admin menu for super admin
    if user_id == SUPER_ADMIN_ID:
        keyboard.append(["⚙️ Admin"])
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_accounts_menu() -> InlineKeyboardMarkup:
    """Get accounts management menu"""
    keyboard = [
        [InlineKeyboardButton("📊 View Status", callback_data="accounts_status")],
        [InlineKeyboardButton("🔐 Authorize Account", callback_data="accounts_authorize")],
        [InlineKeyboardButton("🔄 Reactivate Accounts", callback_data="accounts_reactivate")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_channels_menu() -> InlineKeyboardMarkup:
    """Get channels menu"""
    keyboard = [
        [InlineKeyboardButton("➕ Create Channel", callback_data="channels_create")],
        [InlineKeyboardButton("🔗 Join Channels", callback_data="channels_join")],
        [InlineKeyboardButton("👁️ View Posts", callback_data="channels_view")],
        [InlineKeyboardButton("❤️ React to Posts", callback_data="channels_react")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_groups_menu() -> InlineKeyboardMarkup:
    """Get groups menu"""
    keyboard = [
        [InlineKeyboardButton("➕ Create Group", callback_data="groups_create")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_reports_menu() -> InlineKeyboardMarkup:
    """Get reports menu"""
    keyboard = [
        [InlineKeyboardButton("⚡ Quick Report", callback_data="reports_quick")],
        [InlineKeyboardButton("🔄 Continuous Campaign", callback_data="reports_continuous")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_menu() -> InlineKeyboardMarkup:
    """Get admin menu"""
    keyboard = [
        [InlineKeyboardButton("👥 View Users", callback_data="admin_users")],
        [InlineKeyboardButton("⏳ Pending Approvals", callback_data="admin_pending")],
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
        [InlineKeyboardButton("📢 Broadcast Message", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_confirmation_keyboard(confirm_data: str, cancel_data: str = "cancel") -> InlineKeyboardMarkup:
    """Get confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data=confirm_data),
            InlineKeyboardButton("❌ Cancel", callback_data=cancel_data)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Get cancel keyboard"""
    keyboard = [
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard(callback_data: str = "menu_main") -> InlineKeyboardMarkup:
    """Get back button keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔙 Back", callback_data=callback_data)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_emoji_picker() -> InlineKeyboardMarkup:
    """Get emoji picker for reactions"""
    keyboard = [
        [
            InlineKeyboardButton("👍", callback_data="emoji_👍"),
            InlineKeyboardButton("❤️", callback_data="emoji_❤️"),
            InlineKeyboardButton("🔥", callback_data="emoji_🔥"),
            InlineKeyboardButton("👏", callback_data="emoji_👏")
        ],
        [
            InlineKeyboardButton("😂", callback_data="emoji_😂"),
            InlineKeyboardButton("😮", callback_data="emoji_😮"),
            InlineKeyboardButton("😢", callback_data="emoji_😢"),
            InlineKeyboardButton("🤔", callback_data="emoji_🤔")
        ],
        [
            InlineKeyboardButton("💯", callback_data="emoji_💯"),
            InlineKeyboardButton("🎉", callback_data="emoji_🎉"),
            InlineKeyboardButton("⚡", callback_data="emoji_⚡"),
            InlineKeyboardButton("Custom emoji", callback_data="emoji_custom")
        ],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_report_reasons() -> InlineKeyboardMarkup:
    """Get report reasons keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔞 Pornography", callback_data="reason_porn")],
        [InlineKeyboardButton("⚠️ Violence", callback_data="reason_violence")],
        [InlineKeyboardButton("👶 Child Abuse", callback_data="reason_child_abuse")],
        [InlineKeyboardButton("🚫 Spam", callback_data="reason_spam")],
        [InlineKeyboardButton("💊 Illegal Drugs", callback_data="reason_drugs")],
        [InlineKeyboardButton("© Copyright", callback_data="reason_copyright")],
        [InlineKeyboardButton("📝 Other", callback_data="reason_other")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_task_refresh_keyboard(task_id: str) -> InlineKeyboardMarkup:
    """Get task monitoring keyboard with refresh and stop buttons"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data=f"task_refresh_{task_id}"),
            InlineKeyboardButton("🛑 Stop", callback_data=f"task_stop_{task_id}")
        ],
        [InlineKeyboardButton("🔙 Back to Tasks", callback_data="tasks_list")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_account_selection_keyboard(mode: str = "auto") -> InlineKeyboardMarkup:
    """Get account selection mode keyboard"""
    keyboard = [
        [InlineKeyboardButton("🤖 Auto Select", callback_data=f"accounts_mode_auto_{mode}")],
        [InlineKeyboardButton("✋ Manual Select", callback_data=f"accounts_mode_manual_{mode}")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)
