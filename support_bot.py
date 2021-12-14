import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def answer(update: Update, context: CallbackContext) -> None:
    """Answer the user message."""
    user = update.effective_user
    answer_text = get_dialogflow_answer(
        project_id=context.bot_data['dialogflow_project_id'],
        session_id=user.id,
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


def get_dialogflow_answer(project_id, session_id, text, language_code='ru-RU'):
    """Returns the result of detect intent with text as input."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={
            'session': session,
            'query_input': query_input,
        },
    )

    return response.query_result.fulfillment_text


def main():
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
