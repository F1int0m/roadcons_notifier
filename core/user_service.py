from typing import Optional, Tuple

from peewee import DoesNotExist

from common.db.basic import manager
from common.enums import UserRole
from common.models.db_models import Project, ProjectToUser, User


async def user_create_or_get(user_id: int) -> Tuple[User, bool]:
    return await manager.get_or_create(User, telegram_id=user_id)


async def user_get_by_username(username: str, project: Project) -> Optional[User]:
    try:
        project_to_user: ProjectToUser = await manager.get(ProjectToUser, project=project, username=username)
    except DoesNotExist:
        return None

    return project_to_user.user


async def user_to_project_create_or_get(
        project_id: str,
        user_id: int,
        username: str,
        role: UserRole = UserRole.user
) -> ProjectToUser:
    user, _ = await user_create_or_get(user_id=user_id)

    return await manager.get_or_create(
        ProjectToUser,
        project=project_id,
        user=user.telegram_id,
        defaults={
            'username': username,
            'role': role
        }
    )
