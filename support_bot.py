import logging

from environs import Env
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def config_logger(logger: logging.Logger) -> None:
    """Configures logger."""
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)


def main():
    """Configures and launches the bot."""
    config_logger(logger)

    env = Env()
    env.read_env()
    tg_bot_token = env('tg_bot_token')

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
