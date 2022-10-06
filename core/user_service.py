from typing import Tuple

from common.db.basic import manager
from common.enums import UserRole
from common.models.db_models import ProjectToUser, User


async def user_create_or_get(user_id: int) -> Tuple[User, bool]:
    return await manager.get_or_create(User, telegram_id=user_id)


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
