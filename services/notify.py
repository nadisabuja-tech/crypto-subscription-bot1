from database import cursor


async def broadcast(bot, text):
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    sent = 0
    failed = 0

    for (user_id,) in users:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=text,
            )
            sent += 1
        except Exception:
            failed += 1

    return sent, failed
