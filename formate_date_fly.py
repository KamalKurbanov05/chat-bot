from calendar import Calendar, weekday, monthrange
import datetime
from collections import OrderedDict

CALENDAR_TEXT = Calendar()
FOR_YEAR = datetime.datetime.now().year
FOR_MONTH = datetime.datetime.now().month
FOR_DAY = datetime.datetime.now().day
WEEK_DAY = weekday(year=FOR_YEAR, month=FOR_MONTH, day=FOR_DAY)
DATE_TEST = datetime.datetime(FOR_YEAR, FOR_MONTH, FOR_DAY)
DATE_FOR_TEST = datetime.datetime.strftime(DATE_TEST, '%d-%m-%Y')


def citys():
    city_departure = {
        'моск':
            {
                'full_name': 'москва',
                'рейсы': {
                    'минск': form_the_date(interval=2, hour=15, minute=00),
                    'стамбул': form_the_date(interval=2, hour=15, minute=00),
                    'киев': form_the_date(interval=2, hour=15, minute=00)
                }},

        'лонд':
            {
                'full_name': 'лондон',
                'рейсы': {
                    'париж': form_the_date(interval=3, hour=12, minute=35),
                    'амстердам': form_the_date(interval=2, hour=15, minute=00),
                    'будапешт': form_the_date(interval=2, hour=15, minute=00)
                }},

        'нью-':
            {
                'full_name': 'нью-йорк',
                'рейсы': {
                    'вашингтон': form_the_date(interval=1, hour=10, minute=15),
                    'ласвегас': form_the_date(interval=2, hour=15, minute=00),
                    'аляска': form_the_date(interval=2, hour=15, minute=00)
                }},
    }

    return city_departure


def converts_returns_for_user(text, scenario_time):
    """
        функция для преобразования объектам datetime в привычный для пользователся вид
        type scenario_time: object_datetime

    """

    list_date = []
    date_dict = OrderedDict()

    convert_date_user = datetime.datetime.strptime(text, '%d-%m-%Y')
    for date in scenario_time:
        if isinstance(date, datetime.datetime):
            convert_date = datetime.datetime(date.year, date.month, date.day)
        else:
            convert_date = datetime.datetime.strptime(date[:10], '%d-%m-%Y')

        if convert_date_user == convert_date:
            if isinstance(convert_date, datetime.datetime):
                date_dict[1] = datetime.datetime.strftime(date, '%d-%m-%Y %H:%M')

            else:
                date_dict[1] = date
        else:
            if convert_date_user.month <= convert_date.month:
                if isinstance(date, datetime.datetime):
                    list_date.append(datetime.datetime.strftime(date, '%d-%m-%Y %H:%M'))
                else:
                    list_date.append(date)
                if len(list_date) >= 10:
                    for index, date in enumerate(list_date):

                        if index != 0:
                            date_dict[index] = list_date[index - 1]

                    return date_dict

    for index, date in enumerate(list_date):
        if index != 0:
            date_dict[index] = list_date[index - 1]
    return date_dict


def form_the_date(interval, hour, minute):
    days = 28
    date = datetime.datetime.now()
    for_y = date.year
    for_m = date.month
    for_d = date.day
    count_day_of_month = monthrange(for_y, for_m)[1]
    """
    interval : интервал вылетов    
    """
    departure = []
    for day in range(1, days):
        if day + for_d > count_day_of_month:
            if for_m == 12:
                for_m = 0
            fly = datetime.datetime(for_y, for_m + 1, (day + for_d) - count_day_of_month, hour,
                                    minute)
            departure.append(fly)
        else:
            if (for_d + day) % interval == 0:
                departure.append(datetime.datetime(for_y, for_m, for_d + day, hour, minute))

    return departure


def compare_number(text, list_number):
    """
    :param text: текст пришедший от юзера (юзер по сценарию отравляет номер рейса)
    :param list_number: номера рейсов
    :return:
    """
    if text in list_number:
        return text
    else:
        return False


def date_departure_for_week():
    # функция возращает даты которые приходятся только на среду и пятницу
    # wednesday = None
    # friday = None
    departure_day = []
    for day in CALENDAR_TEXT.itermonthdays2(FOR_YEAR, FOR_MONTH):
        if FOR_DAY < day[0]:
            if day[0] != 0 and day[1] == 2:
                wednesday = datetime.datetime(year=FOR_YEAR, month=FOR_MONTH, day=day[0], hour=10)
                departure_day.append(wednesday)
            elif day[0] != 0 and day[1] == 4:
                friday = datetime.datetime(year=FOR_YEAR, month=FOR_MONTH, day=day[0], hour=10)
                departure_day.append(friday)
    if len(departure_day) != 2:
        for day in CALENDAR_TEXT.itermonthdays2(FOR_YEAR, FOR_MONTH + 1):
            if len(departure_day) == 2:
                return departure_day
            if day[0] != 0 and day[1] == 2:
                wednesday = datetime.datetime(year=FOR_YEAR, month=FOR_MONTH + 1, day=day[0],
                                              hour=10)
                departure_day.append(wednesday)
                return departure_day
            elif day[0] != 0 and day[1] == 4:
                friday = datetime.datetime(year=FOR_YEAR, month=FOR_MONTH + 1, day=day[0],
                                           hour=10)

                departure_day.append(friday),
                return departure_day
    else:
        return departure_day


# функция фомирует вылеты с переодичностью 2 раза в месяц
def date_departure_for_month(first_date, second_date, hour, minute):
    first_month_fly = None
    second_month_fly = None
    global FOR_MONTH
    departure_day = []
    if FOR_DAY > first_date:
        if FOR_MONTH == 12:
            FOR_MONTH = 0
        first_month_fly = datetime.datetime(year=FOR_YEAR, month=FOR_MONTH + 1, day=first_date,
                                            hour=hour, minute=minute)
        departure_day.append(first_month_fly)
    else:
        first_month_fly = datetime.datetime(year=FOR_YEAR, month=FOR_MONTH, day=first_date,
                                            hour=hour, minute=minute)
        departure_day.append(first_month_fly)
    if FOR_DAY > second_date:
        if FOR_MONTH == 12:
            FOR_MONTH = 0
        second_month_fly = datetime.datetime(year=FOR_YEAR, month=FOR_MONTH + 1, day=second_date,
                                             hour=hour, minute=minute)
        departure_day.append(second_month_fly)
    else:
        second_month_fly = datetime.datetime(year=FOR_YEAR, month=FOR_MONTH, day=second_date,
                                             hour=hour, minute=minute)
        departure_day.append(second_month_fly)
    return departure_day


JSON_DATA_CITYS = citys()

