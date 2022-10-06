from logging import getLogger

from telegram.ext import ContextTypes

import config
from common.clients.google_sheet_client import (
    LIST_TO_STATUS_COLUMN,
    LIST_TO_STREET_NAME,
    LIST_TO_USER_COLUM,
    LISTS_TO_READ,
    GoogleSheetClient,
)
from common.db.basic import manager
from common.models.db_models import Project
from common.utils import format_alert_message, utc_now, uuid_str
from core.project_service import get_or_create_last_known_record
from core.user_service import user_get_by_username

log = getLogger(__name__)


async def update_projects(context: ContextTypes.DEFAULT_TYPE):
    log.info('Start updates')
    google_sheet_client: GoogleSheetClient = context.bot_data.get('google_sheet_client')
    project_ids = await manager.execute(Project.select(Project.project_id))

    for project_id in project_ids:
        async with manager.atomic():
            project: Project = next(iter(await manager.execute(
                Project.select().for_update(nowait=True).where(Project.project_id == project_id)
            )))
            log.info(f'Process {project.project_name}')

            for list_name in LISTS_TO_READ:
                usernames = google_sheet_client.get_range(
                    spreadsheet_id=project.project_id,
                    sheet_name=list_name,
                    range=LIST_TO_USER_COLUM[list_name]
                )
                statuses = google_sheet_client.get_range(
                    spreadsheet_id=project.project_id,
                    sheet_name=list_name,
                    range=LIST_TO_STATUS_COLUMN[list_name]
                )
                street_names = google_sheet_client.get_range(
                    spreadsheet_id=project.project_id,
                    sheet_name=list_name,
                    range=LIST_TO_STREET_NAME[list_name]
                )

                for username, status, street_name in zip(usernames, statuses, street_names):
                    last_known_record, created = await get_or_create_last_known_record(
                        project=project,
                        sheet=list_name,
                        street_name=street_name,
                        status=status
                    )
                    if not created:
                        if status != last_known_record.last_known_status:
                            log.info(
                                (f'Found changed status on project={project.project_name} {list_name=} '
                                 f'{username=} {street_name=} {status=}')
                            )
                            user = await user_get_by_username(username=username, project=project)
                            if not user:
                                log.info('User not found')
                                return

                            context.job_queue.run_once(
                                callback=send_message,
                                when=config.NOTIFICATION_DELAY,
                                name=uuid_str(),
                                chat_id=user.telegram_id,
                                data=format_alert_message(
                                    project=project.project_name,
                                    sheet=list_name,
                                    street_name=street_name,
                                    status=status,
                                )
                            )
                            await last_known_record.update_instance(last_known_status=status, last_seen_at=utc_now())
                            log.info('Status updated')


async def send_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(context.job.chat_id, text=context.job.data)
    log.info('message send succesfull')
