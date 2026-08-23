from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, CallbackQueryHandler
from config import (
    TRC20_WALLET,
    BEP20_WALLET,
    SUBSCRIPTION_PRICE,
    ADMIN_CHAT_ID,
)

async def buy_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 USDT (TRC20)", callback_data="trc20")],
        [InlineKeyboardButton("🟡 USDT (BEP20)", callback_data="bep20")],
    ]

    await update.message.reply_text(
        "💳 Choose Payment Network:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "trc20":
        await query.message.reply_text(
            f"🔴 USDT (TRC20)\n\n"
            f"💰 Amount: {SUBSCRIPTION_PRICE} USDT\n\n"
            f"🏦 Wallet:\n{TRC20_WALLET}\n\n"
            f"📸 Payment করার পরে Screenshot পাঠান।"
        )

    elif query.data == "bep20":
        await query.message.reply_text(
            f"🟡 USDT (BEP20)\n\n"
            f"💰 Amount: {SUBSCRIPTION_PRICE} USDT\n\n"
            f"🏦 Wallet:\n{BEP20_WALLET}\n\n"
            f"📸 Payment করার পরে Screenshot পাঠান।"
        )

async def receive_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1].file_id
    user = update.effective_user

    caption = (
        f"💳 New Payment Screenshot\n\n"
        f"👤 User: @{user.username}\n"
        f"🆔 ID: {user.id}"
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ]

    await context.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=photo,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    await update.message.reply_text(
        "✅ Screenshot received.\n\nYour payment is under review by the admin."
    )
