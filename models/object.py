class ObjectMetadata:
    def __init__(self, name, obj_type, size, last_modified, created_at, path):
        self.name = name
        self.type = obj_type
        self.size = size
        self.last_modified = last_modified
        self.created_at = created_at
        self.path = path

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'last_modified': self.last_modified,
            'created_at': self.created_at,
            'path': self.path
        }
