class SingletonPermissionGroup(object):

    def __init__(self, *class_permissions, permission_level: int):
        self.class_permissions = class_permissions
        self.permission_level = permission_level
    
    def has_permission(self, required_permission: int):
        try:
            return self.permission_level >= required_permission
        except TypeError:
            return False

    def __str__(self):
        pass
