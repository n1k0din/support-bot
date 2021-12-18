import logging

from environs import Env
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from dialogflow import get_dialogflow_answer
from telegram_monitoring import config_logger

logger = logging.getLogger('TG_SUPPORT_BOT')


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def answer(update: Update, context: CallbackContext) -> None:
    """Answer the user message."""
    user = update.effective_user
    _is_fallback, answer_text = get_dialogflow_answer(
        project_id=context.bot_data['dialogflow_project_id'],
        session_id=str(user.id),
        text=update.message.text,
    )

    update.message.reply_text(answer_text)


def main() -> None:
    """Configures and launches the bot."""
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    dialogflow_project_id = env('DIALOGFLOW_PROJECT_ID')
    tg_monitoring_bot_token = env('TG_MONITORING_BOT_TOKEN')
    tg_notifications_chat_id = env('TG_NOTIFICATIONS_CHAT_ID')

    config_logger(logger, tg_monitoring_bot_token, tg_notifications_chat_id)

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['dialogflow_project_id'] = dialogflow_project_id

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    while True:
        try:
            logger.info('Бот запускается.')
            updater.start_polling()
            updater.idle()
        except TelegramError:
            logger.exception('А у бота ошибка!')


if __name__ == '__main__':
    main()
