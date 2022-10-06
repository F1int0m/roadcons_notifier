from telegram.ext import Application, CommandHandler

import config
from core import telegram_handlers


def main():
    print('Start init')
    application = Application.builder().token(config.BOT_TOKEN).build()

    welcome_handler = CommandHandler(command=['start', 'help'], callback=telegram_handlers.start)

    application.add_handler(handler=welcome_handler)

    print('Init done')
    application.run_polling()


if __name__ == '__main__':
    main()
