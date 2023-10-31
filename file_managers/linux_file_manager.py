from file_managers.base_file_manager import BaseFileManager
from models.object import ObjectMetadata
import os
import time


class LinuxFileManager(BaseFileManager):
    def make_directory(folder_path, exist_ok=True):
        os.makedirs(folder_path, exist_ok=exist_ok)

    def get_object_metadata(path):
        if os.path.isdir(path):
            item_type = 'folder'
        else:
            item_type = 'file'

        name = os.path.basename(path)

        return ObjectMetadata(
            name=name,
            obj_type=item_type,
            size=os.path.getsize(path),
            last_modified=time.ctime(os.path.getmtime(path)),
            created_at=time.ctime(os.path.getctime(path)),
            path=path
        )

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
            object_metadata = LinuxFileManager.get_object_metadata(
                os.path.join(directory, item))

            if object_metadata.type == 'file' and not show_files:
                continue
            if object_metadata.type == 'folder' and not show_folders:
                continue
            items.append(object_metadata.to_dict())
        return items

    def save_file(path, file, create_folders):
        if create_folders:
            LinuxFileManager.make_directory(
                os.path.dirname(path), exist_ok=True)
        file.save(path)
        return LinuxFileManager.get_object_metadata(path)
