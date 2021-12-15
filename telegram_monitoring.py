import logging

import telegram


class TelegramLogsHandler(logging.Handler):
    """Handler for sending messages via telegram bot."""

    def __init__(self, token: str, chat_id: str) -> None:
        """Inits bot and chat id."""
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=token)

    def emit(self, record: logging.LogRecord) -> None:
        """Sends logger message to bot."""
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def config_logger(logger: logging.Logger, telegram_token: str, telegram_chat_id: str) -> None:
    """Configures logger."""
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    tg_handler = TelegramLogsHandler(telegram_token, telegram_chat_id)
    tg_log_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    tg_handler.setFormatter(tg_log_formatter)
    logger.addHandler(tg_handler)
