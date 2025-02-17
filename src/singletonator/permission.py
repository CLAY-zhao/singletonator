class SingletonPermissionGroup(object):

    def __init__(self, *class_permissions, permission_level: int):
        self.class_permissions = class_permissions
        self.permission_level = permission_level
    
    def has_permission(self, required_permission: int):
        return required_permission >= self.permission_level
    