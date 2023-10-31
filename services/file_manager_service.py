from file_managers.linux_file_manager import LinuxFileManager


class FileManagerService:
    def make_directory(folder_path, exist_ok=True):
        LinuxFileManager.make_directory(folder_path, exist_ok=exist_ok)

    def list_files(path_prefix, show_files=True, show_folders=True):
        return LinuxFileManager.list_files(path_prefix, show_files, show_folders)

    def get_object_metadata(path):
        return LinuxFileManager.get_object_metadata(path)

    def save_file(path, file, create_folders=True):
        return LinuxFileManager.save_file(path, file, create_folders)
