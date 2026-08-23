from datetime import datetime

from database import cursor, conn


def check_subscription(user_id):
    cursor.execute(
        "SELECT subscription, expiry_date FROM users WHERE user_id=?",
        (user_id,),
    )

    user = cursor.fetchone()

    if not user:
        return False

    subscription, expiry_date = user

    if subscription != 1:
        return False

    if not expiry_date:
        return False

    today = datetime.now().date()
    expiry = datetime.strptime(
        expiry_date,
        "%Y-%m-%d",
    ).date()

    if today > expiry:
        cursor.execute(
            """
            UPDATE users
            SET subscription=0,
                expiry_date=NULL
            WHERE user_id=?
            """,
            (user_id,),
        )
        conn.commit()
        return False

    return True
