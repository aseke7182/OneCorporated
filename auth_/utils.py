from datetime import datetime


def get_today_total_age(birthday_date: datetime):
    today = datetime.today()

    return today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
