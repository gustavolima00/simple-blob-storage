from abc import ABC, abstractmethod


class BaseFileManager(ABC):

    @abstractmethod
    def make_directory(folder_path, exist_ok):
        pass

    @abstractmethod
    def list_files(path_prefix, show_files, show_folders):
        pass
