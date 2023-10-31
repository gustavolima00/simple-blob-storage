from datetime import datetime

class ObjectMetadata:
    def __init__(self, name, obj_type, size, last_modified, created_at, path):
        self.name = name
        self.type = obj_type
        self.size = size
        self.last_modified = self.ensure_datetime(last_modified)
        self.created_at = self.ensure_datetime(created_at)
        self.path = path

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'last_modified': self.last_modified.isoformat(),
            'created_at': self.created_at.isoformat(),
            'path': self.path
        }

    def ensure_datetime(self, date):
        if not isinstance(date, datetime):
            return datetime.strptime(date, '%a %b %d %H:%M:%S %Y')
        return date
