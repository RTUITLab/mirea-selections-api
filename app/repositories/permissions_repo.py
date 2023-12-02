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
    def get_permissions() -> list[Permission]:
        return _permissions
