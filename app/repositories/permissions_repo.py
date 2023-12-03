from uuid import UUID, uuid4
from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from app.utils.database import db_dep
from app.schemas import UserPermission
from app.models.user import Permission, PermissionNames


_permissions: list[Permission] = [
    Permission(
        id=PermissionNames.ADMIN,
        title='Управление системой',
        local_description='',
        global_description=''
    ),
    Permission(
        id=PermissionNames.VOTING_ADMIN,
        title='Управление голосованием',
        local_description='',
        global_description=''
    ),
    Permission(
        id=PermissionNames.VOTING_ANALYTICS,
        title='Доступ к аналитике',
        local_description='',
        global_description=''
    ),
    Permission(
        id=PermissionNames.VOTING_EDITOR,
        title='Редактирование номинаций',
        local_description='',
        global_description=''
    ),
    Permission(
        id=PermissionNames.USER_ADMIN,
        title='Управление пользователями',
        local_description='',
        global_description=''
    ),
    Permission(
        id=PermissionNames.USER_VIEWER,
        title='Просмотр пользователей',
        local_description='',
        global_description=''
    ),
]


class PermissionsRepo:
    db: Session

    def __init__(self, db: Session = db_dep) -> None:
        self.db = db

    def get_permissions(self) -> list[Permission]:
        return _permissions

    def add_user_permission(self, user_id: UUID, permission: PermissionNames, voting_id: UUID | None = None) -> bool:
        try:
            print('!!!')
            if permission == PermissionNames.ADMIN and voting_id != None:
                self.db.execute(
                    delete(UserPermission).where(
                        UserPermission.permission == PermissionNames.ADMIN and UserPermission.voting_id == voting_id)
                )
            print('!!!!!')
            

            self.db.add(
                UserPermission(permission=permission, voting_id=voting_id, user_id=user_id, id=uuid4())
            )

            self.db.commit()
            return True
        except:
            import traceback
            print(traceback.print_exc())
            return False
