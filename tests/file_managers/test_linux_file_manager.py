import os
import shutil
import pytest
from hypothesis import given
from hypothesis import strategies as st
from file_managers.linux_file_manager import InvalidDirectoryNameException, InvalidFileNameException, LinuxFileManager
from tests.file_managers.file_manager_test_generator import invalid_directory_names, invalid_file_names, valid_directory_names, valid_file_names


@pytest.fixture(autouse=True)
def setup_and_cleanup():
    os.environ['BASE_FOLDER_PATH'] = './test_uploads'

    yield

    if os.path.exists(LinuxFileManager.base_folder_path()):
        shutil.rmtree(LinuxFileManager.base_folder_path())


@given(valid_directory_names())
def test_make_directory_creates_directory(path):
    full_path = os.path.join(LinuxFileManager.base_folder_path(), path)
    LinuxFileManager.make_directory(path)
    assert os.path.exists(full_path)


@given(invalid_directory_names())
def test_make_directory_raises_exception_for_invalid_directory_names(path):
    try:
        LinuxFileManager.make_directory(path)
        assert False
    except InvalidDirectoryNameException:
        assert True


@given(valid_directory_names(), valid_file_names(), st.binary())
def test_save_file_creates_file(path, file_name, content):
    object_metadata = LinuxFileManager.save_file(path, file_name, content)
    full_path = os.path.join(
        LinuxFileManager.base_folder_path(), path, file_name)
    assert os.path.exists(full_path)
    with open(full_path, 'rb') as file:
        assert file.read() == content
    assert object_metadata.name == file_name
    assert object_metadata.type == 'file'
    assert object_metadata.path == os.path.join(path, file_name)


@given(valid_directory_names(), invalid_file_names(), st.binary())
def test_save_file_raises_exception_for_invalid_file_names(path, file_name, content):
    try:
        LinuxFileManager.save_file(path, file_name, content)
        assert False
    except InvalidFileNameException:
        assert True


@given(invalid_directory_names(), valid_file_names(), st.binary())
def test_save_file_raises_exception_for_invalid_directory_names(path, file_name, content):
    try:
        LinuxFileManager.save_file(path, file_name, content)
        assert False
    except InvalidDirectoryNameException:
        assert True
