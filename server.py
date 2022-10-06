from logging import getLogger

from telegram.ext import Application, CommandHandler

import config
from common import db
from core import telegram_handlers

log = getLogger(__name__)


def main():
    log.info('Telegram init')
    application = Application.builder().token(config.BOT_TOKEN).build()

    handlers = [
        CommandHandler(command=['start', 'help'], callback=telegram_handlers.start),
        CommandHandler(command=['project_load'], callback=telegram_handlers.project_load),
        CommandHandler(command=['project_register'], callback=telegram_handlers.project_register),
    ]

    application.add_handlers(handlers=handlers)
    application.add_error_handler(callback=telegram_handlers.error_handler)

    log.info('DB init')
    application.bot_data.update(
        {'db': db.start()}
    )

    log.info('Init done')
    application.run_polling()


if __name__ == '__main__':
    main()
