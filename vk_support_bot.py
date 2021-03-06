import random
import logging

import vk_api as vk
from environs import Env
from vk_api.longpoll import Event, VkEventType, VkLongPoll
from vk_api.vk_api import VkApiMethod

from dialogflow import get_dialogflow_answer
from telegram_monitoring import config_logger

logger = logging.getLogger('VK_SUPPORT_BOT')


def answer(dialogflow_project_id: str, event: Event, vk_api: VkApiMethod) -> None:
    """Answer the user message."""
    is_fallback, answer_text = get_dialogflow_answer(
        project_id=dialogflow_project_id,
        session_id=str(event.user_id),
        text=event.text,
    )

    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer_text,
            random_id=random.randint(1, 1000),
        )


if __name__ == '__main__':
    env = Env()
    env.read_env()

    vk_token = env('VK_TOKEN')
    dialogflow_project_id = env('DIALOGFLOW_PROJECT_ID')
    tg_monitoring_bot_token = env('TG_MONITORING_BOT_TOKEN')
    tg_notifications_chat_id = env('TG_NOTIFICATIONS_CHAT_ID')

    config_logger(logger, tg_monitoring_bot_token, tg_notifications_chat_id)

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    while True:
        try:
            logger.info('Бот запускается.')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    answer(dialogflow_project_id, event, vk_api)
        except Exception:
            logger.exception('А у бота ошибка!')
