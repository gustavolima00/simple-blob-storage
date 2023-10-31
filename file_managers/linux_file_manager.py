from file_managers.base_file_manager import BaseFileManager
from models.object import Object
import os
import time


class LinuxFileManager(BaseFileManager):
    def make_directory(folder_path, exist_ok=True):
        os.makedirs(folder_path, exist_ok=exist_ok)

    def list_files(path_prefix, show_files, show_folders):
        if os.path.isdir(path_prefix):
            directory = path_prefix
            prefix = ''
        else:
            directory = os.path.dirname(path_prefix)
            prefix = os.path.basename(path_prefix)
            if not os.path.isdir(directory):
                return []

        items = []
        for item in os.listdir(directory):
            if not item.startswith(prefix):
                continue
            item_path = os.path.join(directory, item)

            if os.path.isdir(item_path):
                item_type = 'folder'
            else:
                item_type = 'file'

            if item_type == 'file' and not show_files:
                continue
            if item_type == 'folder' and not show_folders:
                continue

            object_instance = Object(
                name=item,
                obj_type=item_type,
                size=os.path.getsize(item_path),
                last_modified=time.ctime(os.path.getmtime(item_path)),
                created_at=time.ctime(os.path.getctime(item_path)),
                path=item_path
            )
            items.append(object_instance.to_dict())
        return items
