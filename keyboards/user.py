from telegram import ReplyKeyboardMarkup

def main_menu():
    keyboard = [
        ["💳 Buy Subscription", "👤 Profile"],
        ["🔗 Submit Link", "ℹ️ Help"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
