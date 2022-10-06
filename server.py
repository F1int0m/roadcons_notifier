from logging import getLogger

from telegram.ext import Application, CommandHandler

import config
from common import db
from common.clients.google_sheet_client import GoogleSheetClient
from core import telegram_handlers

log = getLogger(__name__)


def main():
    log.info('Telegram init')
    application = Application.builder().token(config.BOT_TOKEN).build()

    handlers = [
        CommandHandler(command=['start', 'help'], callback=telegram_handlers.start),
        CommandHandler(command=['project_load'], callback=telegram_handlers.project_load),
        CommandHandler(command=['project_register'], callback=telegram_handlers.project_register),
        CommandHandler(command=['start_jobs'], callback=telegram_handlers.start_jobs),
        CommandHandler(command=['stop_jobs'], callback=telegram_handlers.stop_jobs),
    ]

    application.add_handlers(handlers=handlers)

    log.info('DB init')
    application.bot_data.update(
        {'db': db.start()}
    )

    log.info('Client init')
    application.bot_data.update(
        {'google_sheet_client': GoogleSheetClient()}
    )

    log.info('Init done')
    application.run_polling()


if __name__ == '__main__':
    main()
