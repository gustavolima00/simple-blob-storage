class Object:
    def __init__(self, name, obj_type, size, last_modified, key):
        self.name = name
        self.type = obj_type
        self.size = size
        self.last_modified = last_modified
        self.key = key

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'last_modified': self.last_modified,
            'key': self.key
        }
