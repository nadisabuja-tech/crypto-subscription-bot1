from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from database import cursor, conn
from datetime import datetime, timedelta


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not admin.")
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE subscription=1")
    active_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE subscription=0")
    inactive_users = cursor.fetchone()[0]

    await update.message.reply_text(
        "🛠 ADMIN PANEL\n\n"
        f"👥 Total Users: {total_users}\n"
        f"✅ Active Users: {active_users}\n"
        f"❌ Inactive Users: {inactive_users}\n\n"
        "Use the payment buttons to approve or reject payments."
    )


async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if update.effective_user.id != ADMIN_ID:
        return

    if query.data.startswith("approve_"):
        user_id = int(query.data.split("_")[1])

        expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        cursor.execute(
            "UPDATE users SET subscription=?, expiry_date=? WHERE user_id=?",
            (1, expiry, user_id),
        )
        conn.commit()

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "✅ Payment Approved!\n\n"
                f"Subscription Active Until:\n{expiry}"
            ),
        )

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n✅ APPROVED"
        )

    elif query.data.startswith("reject_"):
        user_id = int(query.data.split("_")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Payment Rejected.\nPlease contact the admin."
        )

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n❌ REJECTED"
        )
