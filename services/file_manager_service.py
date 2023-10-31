from file_managers.linux_file_manager import LinuxFileManager


class FileManagerService:
    def make_directory(folder_path, exist_ok=True):
        LinuxFileManager.make_directory(folder_path, exist_ok=exist_ok)

    def list_files(path_prefix, show_files=True, show_folders=True):
        return LinuxFileManager.list_files(path_prefix, show_files, show_folders)
