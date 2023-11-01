from file_managers.linux_file_manager import LinuxFileManagerException, LinuxFileManager


class FileManagerServiceException(Exception):
    def __init__(self, message):
        super().__init__(message)


class FileManagerService:
    def make_directory(folder_path):
        try:
            LinuxFileManager.make_directory(folder_path)
        except LinuxFileManagerException as e:
            raise FileManagerServiceException(str(e))

    def list_files(path_prefix, show_files=True, show_folders=True):
        return LinuxFileManager.list_files(path_prefix, show_files, show_folders)

    def get_object_metadata(path):
        try:
            return LinuxFileManager.get_object_metadata(path)
        except LinuxFileManagerException as e:
            raise FileManagerServiceException(str(e))

    def save_file(folder_path, file_name, content):
        try:
            return LinuxFileManager.save_file(folder_path, file_name, content)
        except LinuxFileManagerException as e:
            raise FileManagerServiceException(str(e))

    def get_file(file_path):
        try:
            return LinuxFileManager.get_file(file_path)
        except LinuxFileManagerException as e:
            raise FileManagerServiceException(str(e))
