from file_managers.linux_file_manager import LinuxFileDoesNotExistException, LinuxFileManager


class FileDoesNotExistException(Exception):
    def __init__(self, path):
        super().__init__(f'File {path} does not exist')


class FileManagerService:
    def make_directory(folder_path, exist_ok=True):
        LinuxFileManager.make_directory(folder_path, exist_ok=exist_ok)

    def list_files(path_prefix, show_files=True, show_folders=True):
        return LinuxFileManager.list_files(path_prefix, show_files, show_folders)

    def get_object_metadata(path):
        try:
            return LinuxFileManager.get_object_metadata(path)
        except LinuxFileDoesNotExistException:
            raise FileDoesNotExistException(path)

    def save_file(file_path, content, create_folders=True):
        return LinuxFileManager.save_file(file_path, content, create_folders)

    def get_file(file_path):
        try:
            return LinuxFileManager.get_file(file_path)
        except LinuxFileDoesNotExistException:
            raise FileDoesNotExistException(file_path)
