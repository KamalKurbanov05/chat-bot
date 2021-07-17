import re

from draw_ticket import create_ticket
from formate_date_fly import converts_returns_for_user

re_city = re.compile(r'^[\w\-]{3,}$')
re_date = re.compile(r'\d{2}\-\d{2}\-\d{4}')
re_phone_number = re.compile(r'^\d{6,}$')
re_name = re.compile(r'^\w{3,}\s\w{3,}\s\w{3,}$')


def search_handler_city_departure(text, citys, context):
    if re.match(re_city, text):
        city = text.lower()[:4]
        if city in citys:
            context['departure_city'] = city
            print('ГОрод добавлен', context)
            context['departure_city_full_name'] = citys[city]['full_name']
            return True
    else:
        return False


def search_handler_city_arrival(text, citys, context):
    if re.match(re_city, text):

        arrival_city = citys[context['departure_city']]['рейсы']

        if text in arrival_city:
            context['arrival_city'] = text
            return True
        else:
            return False


def search_date_handler(text, citys, context):
    if re.match(re_date, text):
        departure_city = context['departure_city']
        arrival_city = context['arrival_city']
        date_departure = citys[departure_city]['рейсы'][arrival_city]
        context['dates_departure'] = converts_returns_for_user(text=text,
                                                               scenario_time=date_departure)

        date_departure = [[str(num), str(date)] for num, date in context['dates_departure'].items()]
        print("-" * 12)
        print(date_departure)
        context['date_departure_join'] = '\n'.join([' '.join(date) for date in date_departure])

        return True
    else:
        return False


def search_number_date(text, citys, context):
    if text.isdigit():
        if int(text) != 0 and int(text) <= len(context['dates_departure']):
            date = context['dates_departure'][text]
            context['date_departure'] = date
            return True
        else:
            return False
    else:
        return False


def create_and_search_site(text, citys, context):
    if text.isdigit():
        if int(text) != 0 and int(text) <= 5:
            context['sites'] = text
            return True
    else:
        return False


def choose_answer(text, citys, context):
    if text == 'да':
        context['answer'] = 'введите номер телефона'
        return True
    elif text == 'нет':
        return False
    else:
        return False


def number_phone_handler(text, citys, context):
    if re.match(re_phone_number, text):
        context['phone_number'] = text
        context['phone_answer'] = f'вам позвонят по этому номеру {text}'
        return True
    else:
        return False


def name_handler(text, citys, context):
    if re.match(re_name, text):
        context['name'] = text
        return True
    else:
        return False


def generate_ticket(context):
    return create_ticket(context)
