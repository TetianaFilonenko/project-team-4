from datetime import datetime, timedelta
from collections import defaultdict


# Print users for `users` list that have birthday next week
# - print users birthdays for the next week starting from current date
# - users that have birthday on weekend need to be greeted the next Monday
# - week starts from Monday
def get_birthdays_per_week(users):
    current_date = datetime.today().date()
    result = defaultdict(list)
    for user in users:
        user_name = user["name"]
        user_birthday = user["birthday"].date()
        birthday_this_year = prepare_birthday_date(current_date, user_birthday)
        delta_days = (birthday_this_year - current_date).days
        # Check if birthday falls in the next week
        if delta_days < 7:
            update_result(result, user_name, birthday_this_year)
    if not result:
        return "No birthdays next week"
    return "\n".join([f"{date}: {(",").join(people)}" for date, people in result.items()])

# Print users for 'users' list that have birthdays in the next number of days
def get_birthdays_in_next_days(users, days):
    current_date = datetime.today().date()
    result = defaultdict(list)
    for user in users:
        user_name = user["name"]
        user_birthday = user["birthday"].date()
        birthday_this_year = prepare_birthday_date(current_date, user_birthday)
        delta_days = (birthday_this_year - current_date).days
        if delta_days < int(days):
            result_dates(result, user_name, birthday_this_year)
    if not result:
        return f"No birthdays in next {days} days"
    return "\n".join([f"{date}: {(",").join(people)}" for date, people in result.items()])

def get_today_birthday(users):
    current_date = datetime.today().date()
    result = defaultdict(list)
    for user in users:
        user_name = user["name"]
        user_birthday = user["birthday"].date()
        birthday_this_year = prepare_birthday_date(current_date, user_birthday)
        if birthday_this_year == current_date:
            result['Today'].append(user_name)
    if not result:
        return 'Today there is no birthdays'
    return '\n'.join([f'Don`t forget to congratulate: {(',').join(people)}' for people in result.values()])


def result_dates(result, user_name, birthday_this_year):
    day_date = birthday_this_year.strftime('%d %B')
    result[day_date].append(user_name)


def update_result(result, user_name, birthday_this_year):
    day_string = birthday_this_year.strftime('%A')
    result[day_string].append(user_name)


def prepare_birthday_date(current_date, user_birthday):
    try:
        birthday_this_year = user_birthday.replace(year=current_date.year)
    except ValueError:  # For February 29th on non-leap years
        birthday_this_year = user_birthday.replace(year=current_date.year, day=user_birthday.day - 1) + timedelta(
            days=1)
    if birthday_this_year < current_date:
        birthday_this_year = birthday_this_year.replace(year=current_date.year + 1)
    # Adjust for weekends
    if birthday_this_year.weekday() in [5, 6]:
        birthday_this_year += timedelta(days=7 - birthday_this_year.weekday())
    return birthday_this_year


if __name__ == "__main__":
    print(get_birthdays_per_week([
        {"name": "Bill Gates", "birthday": datetime(1981, 3, 14)},
        {"name": "Steve Jobs", "birthday": datetime(1982, 3, 17)},
        {"name": "Tim Cook", "birthday": datetime(1991, 3, 17)},
        {"name": "Jef Bezos", "birthday": datetime(1992, 5, 13)},  # needs to be added to the list next week
        {"name": "Mark Zucherberg", "birthday": datetime(1983, 2, 10)},
    ]))

    print(get_birthdays_in_next_days([
        {"name": "Bill Gates", "birthday": datetime(1981, 3, 13)},
        {"name": "Steve Jobs", "birthday": datetime(1982, 3, 14)},
        {"name": "Tim Cook", "birthday": datetime(1991, 3, 17)},
        {"name": "Jef Bezos", "birthday": datetime(1992, 5, 13)},  # needs to be added to the list next week
        {"name": "Mark Zucherberg", "birthday": datetime(1983, 2, 10)},
    ], 1))
    print(get_today_birthday([
        {"name": "Bill Gates", "birthday": datetime(1981, 3, 14)},
        {"name": "Steve Jobs", "birthday": datetime(1982, 3, 15)},
        {"name": "Tim Cook", "birthday": datetime(1991, 3, 17)},
        {"name": "Jef Bezos", "birthday": datetime(1992, 5, 13)},  # needs to be added to the list next week
        {"name": "Mark Zucherberg", "birthday": datetime(1983, 2, 10)},
              ]))