from logging import getLogger

from peewee import IntegrityError
from telegram import Update
from telegram.ext import ContextTypes

import config
from common.utils import get_project_id_from_url, parse_args_to_link_with_name
from core import project_service, user_service
from jobs.telegram_jobs import update_projects

log = getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет. Я мониторю изменение статусов улиц')


async def project_load(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sheet_link, project_name = parse_args_to_link_with_name(context.args)
    except ValueError:
        await update.message.reply_text('Неверное число аргументов')
        return

    try:
        await project_service.project_create(
            project_name=project_name,
            project_id=get_project_id_from_url(google_sheet_url=sheet_link),
        )
    except IntegrityError:
        await update.message.reply_text('Проект уже существует')
        return
    await update.message.reply_text('Проект создан')


async def project_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sheet_link, username = parse_args_to_link_with_name(context.args)
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


async def start_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_repeating(
        callback=update_projects,
        interval=config.JOB_UPDATE_INTERVAL,
    )
    await update.message.reply_text('Начал следить за всеми проектами')


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from jobs.telegram_jobs import send_message
    context.job_queue.run_once(
        callback=send_message,
        when=10,
        chat_id=update.message.chat_id,
        data='123321'
    )
