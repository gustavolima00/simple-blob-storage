from file_managers.base_file_manager import BaseFileManager
from models.object import ObjectMetadata
import os
import time


class LinuxFileDoesNotExistException(Exception):
    def __init__(self, path):
        super().__init__(f'File {path} does not exist')


class LinuxFileManager(BaseFileManager):
    def __base_folder_path():
        base_folder_path = os.getenv('BASE_FOLDER_PATH', './uploads')
        if not os.path.exists(base_folder_path):
            os.makedirs(base_folder_path, exist_ok=True)
        return base_folder_path

    def make_directory(folder_path, exist_ok=True):
        full_path = os.path.join(
            LinuxFileManager.__base_folder_path(), folder_path)
        os.makedirs(full_path, exist_ok=exist_ok)

    def get_object_metadata(path):
        full_path = os.path.join(LinuxFileManager.__base_folder_path(), path)
        if not os.path.exists(full_path):
            raise LinuxFileDoesNotExistException(full_path)

        if os.path.isdir(full_path):
            item_type = 'folder'
        else:
            item_type = 'file'

        name = os.path.basename(full_path)

        return ObjectMetadata(
            name=name,
            obj_type=item_type,
            size=os.path.getsize(full_path),
            last_modified=time.ctime(os.path.getmtime(full_path)),
            created_at=time.ctime(os.path.getctime(full_path)),
            path=path
        )

    def list_files(path_prefix, show_files, show_folders):
        full_path_prefix = os.path.join(
            LinuxFileManager.__base_folder_path(), path_prefix)

        if os.path.isdir(full_path_prefix):
            directory = full_path_prefix
            prefix = ''
        else:
            directory = os.path.dirname(full_path_prefix)
            prefix = os.path.basename(full_path_prefix)
            if not os.path.isdir(directory):
                return []

        items = []
        for item in os.listdir(directory):
            if not item.startswith(prefix):
                continue
            path_without_base = os.path.relpath(
                os.path.join(directory, item), LinuxFileManager.__base_folder_path())

            object_metadata = LinuxFileManager.get_object_metadata(
                path_without_base)

            if object_metadata.type == 'file' and not show_files:
                continue
            if object_metadata.type == 'folder' and not show_folders:
                continue
            items.append(object_metadata)
        return items

    def save_file(path, file, create_folders):
        full_path = os.path.join(LinuxFileManager.__base_folder_path(), path)
        if create_folders:
            LinuxFileManager.make_directory(
                os.path.dirname(full_path), exist_ok=True)
        file.save(full_path)
        return LinuxFileManager.get_object_metadata(path)
