from abc import ABC, abstractmethod


class BaseFileManager(ABC):

    @abstractmethod
    def make_directory(folder_path, exist_ok):
        pass

    @abstractmethod
    def list_files(path_prefix, show_files, show_folders):
        pass

    @abstractmethod
    def get_object_metadata(path):
        pass

    @abstractmethod
    def write_file(filepath, content, create_folders):
        pass
