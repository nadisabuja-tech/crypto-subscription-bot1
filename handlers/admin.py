from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID
from database import cursor, conn
from services.notify import broadcast


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
        "Commands:\n"
        "/broadcast Your Message"
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


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/broadcast Your message"
        )
        return

    message = " ".join(context.args)

    sent, failed = await broadcast(
        context.bot,
        message,
    )

    await update.message.reply_text(
        f"✅ Broadcast Complete\n\n"
        f"Sent: {sent}\n"
        f"Failed: {failed}"
    )

async def setprice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage:\n/setprice 10")
        return

    price = context.args[0]

    cursor.execute(
        "UPDATE settings SET value=? WHERE key='subscription_price'",
        (price,),
    )
    conn.commit()

    await update.message.reply_text(
        f"✅ Subscription price updated to {price} USDT"
    )


async def settrc20_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage:\n/settrc20 WALLET_ADDRESS")
        return

    wallet = " ".join(context.args)

    cursor.execute(
        "UPDATE settings SET value=? WHERE key='trc20_wallet'",
        (wallet,),
    )
    conn.commit()

    await update.message.reply_text("✅ TRC20 wallet updated.")


async def setbep20_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage:\n/setbep20 WALLET_ADDRESS")
        return

    wallet = " ".join(context.args)

    cursor.execute(
        "UPDATE settings SET value=? WHERE key='bep20_wallet'",
        (wallet,),
    )
    conn.commit()

    await update.message.reply_text("✅ BEP20 wallet updated.")
