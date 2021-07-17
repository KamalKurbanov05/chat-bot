from copy import deepcopy

from random import randint

from pony.orm import db_session, rollback

from unittest import TestCase
from unittest.mock import patch, Mock

from vk_api.bot_longpoll import VkBotMessageEvent

from chat_bot_file import ChatBot

import settings

from formate_date_fly import DATE_FOR_TEST, converts_returns_for_user, form_the_date
from handlers import generate_ticket

USER_MAKE_CHOICE_DATE = str(randint(1, 2))
USER_MAKE_CHOICE_SITES = str(randint(1, 5))

CONTEXT_TEST = {
    "name": "test",
    "arrival_city": "test",
    "date_departure": "test",
    "departure_city_full_name": "test",
}


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()

    return wrapper


class TestBot1(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object':
            {'date': 1593446014, 'from_id': 366826907, 'id': 269, 'out': 0, 'peer_id': 366826907,
             'text': 'некий текст', 'conversation_message_id': 269, 'fwd_messages': [],
             'important': False,
             'random_id': 0, 'attachments': [], 'is_hidden': False},
        'group_id': 195574726}

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_moc = Mock(return_value=events)
        long_poller_moc_listen = Mock()
        long_poller_moc_listen.listen = long_poller_moc
        with patch('chat_bot_file.vk_api.VkApi'):
            with patch('chat_bot_file.VkBotLongPoll', return_value=long_poller_moc_listen):
                vk_bot = ChatBot('', '')
                vk_bot.on_event = Mock()
                vk_bot.send_to_image = Mock()
                vk_bot.run()
                vk_bot.on_event.assert_called()
                vk_bot.on_event.assert_any_call(obj)
                assert vk_bot.on_event.call_count == count

    INPUTS = [
        'привет',
        '/help',
        '/ticket.png',
        'магадан',
        'москва',
        'стамбул',
        DATE_FOR_TEST,
        USER_MAKE_CHOICE_DATE,
        USER_MAKE_CHOICE_SITES,
        'да',
        '12345678',
    ]

    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENT[0]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step1']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step3']['text'],
        settings.SCENARIOS['registration']['steps']['step4']['text'].format(
            date_departure_join='\n'.join(
                [str((num, date)) for num, date in
                 converts_returns_for_user(DATE_FOR_TEST, form_the_date(interval=2, hour=15,
                                                                        minute=00)).items()])),
        settings.SCENARIOS['registration']['steps']['step5']['text'],
        settings.SCENARIOS['registration']['steps']['step6']['text'].format(
            departure_city_full_name='москва',
            arrival_city='стамбул', date_departure=
            converts_returns_for_user(DATE_FOR_TEST,
                                      form_the_date(interval=2, hour=15, minute=00))[
                int(USER_MAKE_CHOICE_DATE)],
            sites=USER_MAKE_CHOICE_SITES),
        settings.SCENARIOS['registration']['steps']['step7']['text'].format(
            name='Мухаммадов Мухаммад Мухаммадович', ),
        settings.SCENARIOS['registration']['steps']['step8']['text'].format(
            answer='введите номер телефона', phone_number='12345678'),
    ]

    @isolate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock
        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['text'] = str(input_text)
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('chat_bot_file.VkBotLongPoll', return_value=long_poller_mock):
            bot = ChatBot('', '')
            bot.api = api_mock
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])

    def test_generate_ticket(self):
        ticket_file = generate_ticket(CONTEXT_TEST)
        print(ticket_file)
        with open('files/example_ticket.png', 'rb') as file_example_ticket:
            expected_bytes = file_example_ticket.read()
            print('expected_bytes =', expected_bytes)
            print('ticket_file =', ticket_file.read())
        assert ticket_file.read() != expected_bytes
