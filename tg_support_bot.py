import logging

from environs import Env
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from dialogflow import get_dialogflow_answer

logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def answer(update: Update, context: CallbackContext) -> None:
    """Answer the user message."""
    user = update.effective_user
    answer_text = get_dialogflow_answer(
        project_id=context.bot_data['dialogflow_project_id'],
        session_id=str(user.id),
        text=update.message.text,
    )

    update.message.reply_text(answer_text)


def config_logger(logger: logging.Logger) -> None:
    """Configures logger."""
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)


def main() -> None:
    """Configures and launches the bot."""
    config_logger(logger)

    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    dialogflow_project_id = env('DIALOGFLOW_PROJECT_ID')

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['dialogflow_project_id'] = dialogflow_project_id

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
