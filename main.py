import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from database import cursor, conn
from handlers.payment import (
    buy_subscription,
    payment_callback,
    receive_screenshot,
)

from handlers.admin import (
    admin_panel,
    admin_callback,
    broadcast_command,
    setprice_command,
    settrc20_command,
    setbep20_command,
)

from handlers.link import (
    ask_link,
    receive_link,
)

TOKEN = os.getenv("BOT_TOKEN")

keyboard = [
    ["💳 Buy Subscription", "👤 Profile"],
    ["🔗 Submit Link", "ℹ️ Help"],
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
        (
            update.effective_user.id,
            update.effective_user.username,
        ),
    )
    conn.commit()

    await update.message.reply_text(
        "👋 Welcome to Crypto Subscription Bot!",
        reply_markup=reply_markup,
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("waiting_link"):
        await receive_link(update, context)
        return

    text = update.message.text

    if text == "💳 Buy Subscription":
        await buy_subscription(update, context)

    elif text == "👤 Profile":
        cursor.execute(
            "SELECT subscription, expiry_date FROM users WHERE user_id=?",
            (update.effective_user.id,),
        )

        user = cursor.fetchone()

        if user and user[0] == 1:
            await update.message.reply_text(
                f"👤 Profile\n\n"
                f"Subscription: ✅ Active\n"
                f"Expiry: {user[1]}"
            )
        else:
            await update.message.reply_text(
                "👤 Profile\n\nSubscription: ❌ Inactive"
            )

    elif text == "🔗 Submit Link":
        cursor.execute(
            "SELECT subscription FROM users WHERE user_id=?",
            (update.effective_user.id,),
        )

        user = cursor.fetchone()

        if user and user[0] == 1:
            await ask_link(update, context)
        else:
            await update.message.reply_text(
                "❌ Please buy a subscription first."
            )

    elif text == "ℹ️ Help":
        await update.message.reply_text(
            "Contact Admin for help."
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("setprice", setprice_command))
    app.add_handler(CommandHandler("settrc20", settrc20_command))
    app.add_handler(CommandHandler("setbep20", setbep20_command))
    app.add_handler(
        MessageHandler(filters.PHOTO, receive_screenshot)
    )

    app.add_handler(
        CallbackQueryHandler(
            admin_callback,
            pattern="^(approve|reject)_",
        )
    )

    app.add_handler(
        CallbackQueryHandler(payment_callback)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu,
        )
    )

    print("✅ Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
