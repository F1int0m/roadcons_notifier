from common.db.basic import manager
from common.models.db_models import Project


async def project_create(project_name: str, project_id: str):
    project = await Project.create(
        project_name=project_name,
        project_id=project_id,
    )
    await update_projects()
    return project


async def update_projects():
    project_ids = await manager.execute(Project.select(Project.project_id))

    for project_id in project_ids:
        async with manager.atomic():
            await manager.execute(
                Project.select().for_update().where(Project.project_id == project_id)
            )


async def project_get(project_id: str) -> Project:
    return await manager.get(Project, project_id=project_id)
