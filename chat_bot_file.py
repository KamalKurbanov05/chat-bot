import logging
import random
import requests
import handlers

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from pony.orm import db_session, commit

from models import UserState, UserData
from formate_date_fly import JSON_DATA_CITYS

try:
    import settings
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')

log = logging.getLogger('chat_bot_file')


def bot_log():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(' - %(levelname)s - %(message)s'))
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)
    file_handler = logging.FileHandler(filename='log_chat_bot.log', mode='a', encoding='UTF-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                                datefmt='%Y-%m-%d %H:%M'))
    log.addHandler(file_handler)
    file_handler.setLevel(logging.DEBUG)
    log.setLevel(logging.DEBUG)


class ChatBot:
    '''
        Echo Bot для vk.com
        User Python 3.8
    '''

    def __init__(self, group_id, token):
        '''
        :param group_id: id с группы vc.com
        :param token: секретный токен
        '''
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        '''Запуск бота'''
        for event in self.long_poller.listen():
            log.info('получно событие')
            try:
                self.on_event(event)

            except Exception:
                log.exception('пойманно исключение')

    @db_session
    def on_event(self, event):
        '''
        возращаем сообщения назад, если это текст
        :param event: event
        :return:
        '''
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.debug('мы пока не умеем обрабатывать такое %s', event.type)
            return
        user_id = event.object.peer_id
        text = event.object.text.lower()
        state = UserState.get(user_id=str(user_id))
        words_break_program = ['/ticket', '/help']
        if state is not None:
            if text in words_break_program:
                text_to_send = r'Вы ввели (/ticket|/help), все введенные данные удалены'
                state.delete()
                self.send_to_text(text_to_send, user_id)
            else:
                self.continue_scenario(text, state, user_id)

        else:
            for intent in settings.INTENT:
                log.debug(f"user get's {intent}")
                if intent['tokens'] == text:
                    if intent['answer']:
                        text_to_send = intent['answer']
                        self.send_to_text(text_to_send, user_id)
                    else:
                        self.start_scenario(str(user_id), intent['scenario'])
                    break
            else:
                self.send_to_text(settings.DEFAULT_ANSWER, user_id)

    def send_to_text(self, send_text, user_id):
        self.api.messages.send(
            message=send_text,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id
        )

    def send_to_image(self, image, user_id):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_data = requests.post(upload_url,
                                    files={'photo': ('image.png', image, 'image/png')}).json()
        image_data = self.api.photos.saveMessagesPhoto(**upload_data)
        owner_id = image_data[0]['owner_id']
        media_id = image_data[0]['id']
        attachment = f'photo{owner_id}_{media_id}'
        self.api.messages.send(
            attachment=attachment,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id
        )

    def send_step(self, step, user_id, text, context):
        if 'text' in step:
            self.send_to_text(step['text'].format(**context), user_id)
        if 'image' in step:
            handler = getattr(handlers, step['image'])
            image = handler(context)
            self.send_to_image(image, user_id)

    def start_scenario(self, user_id, scenario_name):
        scenario = settings.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        UserState(user_id=str(user_id), scenario_name=scenario_name, step_name=first_step,
                  context={})
        self.send_to_text(step['text'], user_id)

    @db_session
    def continue_scenario(self, text, state, user_id):
        steps = settings.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        if handler(text=text, citys=JSON_DATA_CITYS, context=state.context):
            if state.context:
                next_step = steps[step['next_step']]
                self.send_step(next_step, user_id, text, state.context)
                if next_step['next_step']:
                    state.step_name = step['next_step']
                else:
                    UserData(
                        name=state.context['name'],
                        number=state.context['phone_number'],
                        departure_city=state.context['departure_city_full_name'],
                        arrival_city=state.context['arrival_city'],
                        data_departure=state.context['date_departure'],
                        sites=state.context['sites'],
                    )
                    commit()
                    state.delete()
            else:
                state.delete()
                text_to_send = 'оформление билета'
                self.send_to_text(text_to_send, user_id)
        else:
            if text == 'нет':
                state.delete()
                text_to_send = 'вы прервали оформление билета'
                self.send_to_text(text_to_send, user_id)
            else:
                text_to_send = step['failure_text']
                self.send_to_text(text_to_send, user_id)


if __name__ == '__main__':
    bot_log()
    vk_bot = ChatBot(settings.ID_GROUP, settings.TOKEN_VK)
    vk_bot.run()
