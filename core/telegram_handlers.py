import json
import traceback
from logging import getLogger

from telegram import Update
from telegram.ext import ContextTypes

from common.utils import get_project_id_from_url
from core import project_service, user_service

log = getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет. Я мониторю изменение статусов улиц')


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.info(f'Exception while handling an update:{context.error}')

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        'Catch error\n'
        f'Update = {json.dumps(update_str, indent=2, ensure_ascii=False)}\n'
        f'Traceback:\n{tb_string}'
    )

    await context.bot.send_message(chat_id=update.message.chat_id, text=message)


async def project_load(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sheet_link, project_name = context.args
    except ValueError:
        await update.message.reply_text('Неверное число аргументов')
        return

    await project_service.project_create(
        project_name=project_name,
        project_id=get_project_id_from_url(google_sheet_url=sheet_link),
    )

    await update.message.reply_text('Проект создан')


async def project_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sheet_link, username = context.args
    except ValueError:
        await update.message.reply_text('Неверное число аргументов')
        return

    project_id = get_project_id_from_url(sheet_link)
    project = await project_service.project_get(project_id=project_id)

    await user_service.user_to_project_create_or_get(
        project_id=project.project_id,
        user_id=update.message.chat_id,
        username=username
    )

    await update.message.reply_text(f'Добавил в список отслеживания к проекту {project.project_name}')
