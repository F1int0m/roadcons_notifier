from typing import Tuple

from common.db.basic import manager
from common.models.db_models import LastKnownState, Project
from common.utils import utc_now


async def project_create(project_name: str, project_id: str):
    project = await Project.create(
        project_name=project_name,
        project_id=project_id,
    )
    return project


async def project_get(project_id: str) -> Project:
    return await manager.get(Project, project_id=project_id)


async def get_or_create_last_known_record(
        project: Project,
        sheet: str,
        street_name: str,
        status: str
) -> Tuple[LastKnownState, bool]:
    return await manager.get_or_create(
        LastKnownState,
        project=project,
        sheet=sheet,
        street_name=street_name,
        defaults={
            'last_known_status': status,
            'last_seen_at': utc_now()
        }
    )
