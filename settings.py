ID_GROUP = '195574726'
TOKEN_VK = 'e115699f5bddd046d98d024d48a9b5c636f30f2a27143212faff70163b783e32ee7df1f8f208a55bb63d7'

INTENT = [
    {
        'tokens': '/help',
        'scenario': None,
        'answer': 'введите "/ticket" для оформления билета'
    },
    {
        'tokens': '/ticket',
        'scenario': 'registration',
        'answer': None
    },
]
SCENARIOS = {'registration': {
    'first_step':
        'step1',
    'steps': {
        'step1': {
            'text': 'Город с которого будете отправляться',
            'failure_text': 'Такого города нет',
            'handler': 'search_handler_city_departure',
            'next_step': 'step2'

        },
        'step2': {
            'text': 'Город в который будете отправляться',
            'failure_text': 'Такого города нет',
            'handler': 'search_handler_city_arrival',
            'next_step': 'step3'

        },

        'step3': {
            'text': 'Введите дату вылета, формат ввода DD-MM-YYYY',
            'failure_text': 'Некорректыне данные',
            'handler': 'search_date_handler',
            'next_step': 'step4'

        },
        'step4': {
            'text': 'Введите номер который соответствует нужной вам дате\n{date_departure_join}',
            'failure_text': 'Такой даты',
            'handler': 'search_number_date',
            'next_step': 'step5'
        },

        'step5': {
            'text': 'Введите кол-во мест',
            'failure_text': 'Макс. кол-во билетов - 5, мин. - 1',
            'handler': 'create_and_search_site',
            'next_step': 'step6'
        },

        'step6': {
            'text': 'Проверьте введеные вами данные\n'
                    'Вылет из города - {departure_city_full_name}\n прилет в город - {arrival_city}\n '
                    'Дата вылета{date_departure}\n'
                    'Колличество мест - {sites}\n'
                    'Если данные верны, введите "да"\n'
                    'Если желаете прервать оформление билета, введите "нет"',
            'failure_text': 'Введенные данные некорктны, ввести "да"/"нет"',
            'handler': 'choose_answer',
            'next_step': 'step7'
        },

        'step7': {
            'text': 'Введите Ф.И.О',
            'failure_text': 'формат ввода -> Ф.И.О',
            'handler': 'name_handler',
            'next_step': 'step8'
        },

        'step8': {
            'text': '{answer} ',
            'failure_text': 'введите корректный номер',
            'handler': 'number_phone_handler',
            'next_step': 'step9'
        },

        'step9': {
            'text': '{phone_answer}',
            'image': 'generate_ticket',
            'failure_text': None,
            'handler': None,
            'next_step': None
        },

    }}}

DEFAULT_ANSWER = 'бот вас не понял, введите "/help" или "/ticket"'

DB_CONFIG = dict(provider='postgres',
                 user='postgres',
                 host='localhost',
                 password='kamal0468343',
                 database='vk_chat_bot')
