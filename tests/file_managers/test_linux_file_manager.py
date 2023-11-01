import shutil
from hypothesis import given
import hypothesis.strategies as st
import os
from file_managers.linux_file_manager import InvalidDirectoryNameException, LinuxFileManager

def directory_paths():
    path_part = st.text(alphabet=st.characters(blacklist_characters="/\\<>:*?\"|\x00"), min_size=1)
    return st.lists(path_part, min_size=1).map("/".join)

@given(directory_paths())
def test_make_directory_creates_directory(path):
    valid_directory = LinuxFileManager.is_valid_directory_name(path)
    full_path = os.path.join(LinuxFileManager.base_folder_path(), path)
    try:
        LinuxFileManager.make_directory(path)
        assert os.path.exists(full_path)
        shutil.rmtree(full_path)
    except InvalidDirectoryNameException as e:
        assert not valid_directory
        assert not os.path.exists(full_path)
