from models.object_metadata import ObjectMetadata
import os
import time


class LinuxFileManagerException(Exception):
    def __init__(self, message):
        super().__init__(message)


class FileDoesNotExistException(LinuxFileManagerException):
    def __init__(self, path):
        super().__init__(f'File {path} does not exist')


class InvalidDirectoryNameException(LinuxFileManagerException):
    def __init__(self, directory_name):
        super().__init__(f'Invalid directory name: {directory_name}')


class InvalidFileNameException(LinuxFileManagerException):
    def __init__(self, file_name):
        super().__init__(f'Invalid file name: {file_name}')


class LinuxFileManager:
    @staticmethod
    def is_valid_directory_name(directory_name):
        return all(c.isalnum() or c in ('-', '_') for c in directory_name)

    @staticmethod
    def is_valid_file_name(file_name):
        if file_name in [".", ".."]:
            return False
        return all(c.isalnum() or c in ('-', '_', '.') for c in file_name)

    @staticmethod
    def base_folder_path():
        base_folder_path = os.getenv('BASE_FOLDER_PATH', './uploads')
        if not os.path.exists(base_folder_path):
            os.makedirs(base_folder_path, exist_ok=True)
        return base_folder_path

    @staticmethod
    def make_directory(folder_path):
        if not LinuxFileManager.is_valid_directory_name(folder_path):
            raise InvalidDirectoryNameException(folder_path)

        full_path = os.path.join(
            LinuxFileManager.base_folder_path(), folder_path)
        os.makedirs(full_path, exist_ok=True)

    @staticmethod
    def get_object_metadata(path):
        full_path = os.path.join(LinuxFileManager.base_folder_path(), path)
        if not os.path.exists(full_path):
            raise FileDoesNotExistException(path)

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

    @staticmethod
    def list_files(path_prefix, show_files, show_folders):
        full_path_prefix = os.path.join(
            LinuxFileManager.base_folder_path(), path_prefix)

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
                os.path.join(directory, item), LinuxFileManager.base_folder_path())

            object_metadata = LinuxFileManager.get_object_metadata(
                path_without_base)

            if object_metadata.type == 'file' and not show_files:
                continue
            if object_metadata.type == 'folder' and not show_folders:
                continue
            items.append(object_metadata)
        return items

    @staticmethod
    def save_file(folder_path, file_name, content):
        if not LinuxFileManager.is_valid_file_name(file_name):
            raise InvalidFileNameException(file_name)
        if not LinuxFileManager.is_valid_directory_name(folder_path):
            raise InvalidDirectoryNameException(folder_path)
        LinuxFileManager.make_directory(folder_path)
        file_path = os.path.join(folder_path, file_name)
        real_file_path = os.path.join(
            LinuxFileManager.base_folder_path(), file_path)
        with open(real_file_path, 'wb') as file:
            file.write(content)
        return LinuxFileManager.get_object_metadata(file_path)

    @staticmethod
    def get_file(filepath):
        full_path = os.path.join(
            LinuxFileManager.base_folder_path(), filepath)
        if not os.path.exists(full_path):
            raise FileDoesNotExistException(filepath)
        if not os.path.isfile(full_path):
            raise FileDoesNotExistException(filepath)
        content = open(full_path, 'rb')
        metadata = LinuxFileManager.get_object_metadata(filepath)

        return content, metadata
