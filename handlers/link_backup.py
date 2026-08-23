from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_CHAT_ID

async def ask_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_link"] = True

    await update.message.reply_text(
        "🔗 Please send your link."
    )


async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_link"):
        return

    context.user_data["waiting_link"] = False

    user = update.effective_user
    link = update.message.text.strip()

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            "📩 New Link Submission\n\n"
            f"👤 Username: @{user.username}\n"
            f"🆔 User ID: {user.id}\n\n"
            f"🔗 Link:\n{link}"
        ),
    )

    await update.message.reply_text(
        "✅ Link submitted successfully."
    )
