import pytest

from file_data_models.digital_file import DigitalFile
from file_data_models.directory import Directory
from file_data_models.fortran_file import FortranFile


@pytest.fixture
def empty_dir():
    return Directory("empty_dir_fixture")


@pytest.fixture
def populated_dir():
    subdir = Directory("test_subdir")
    file_obj_1 = DigitalFile("test_file")
    file_obj_2 = DigitalFile("test_file_2")

    return Directory("populated_dir_fixture", [subdir], [file_obj_1, file_obj_2])


class TestDirectory:
    def test_directory_bad_init(self):
        with pytest.raises(TypeError):
            test_dir = Directory()  # noqa: F841

    def test_init_empty_dir(self, empty_dir):
        assert empty_dir.name == "empty_dir_fixture"
        assert len(empty_dir.subdirectories) == 0
        assert len(empty_dir.files) == 0

    def test_init_populated_dir(self, populated_dir):
        assert populated_dir.name == "populated_dir_fixture"
        assert len(populated_dir.subdirectories) == 1
        assert len(populated_dir.files) == 2

    def test_add_subdirectory(self, empty_dir):
        dir_to_add = Directory("added_dir")

        assert len(empty_dir.subdirectories) == 0
        empty_dir.add_subdirectory(dir_to_add)
        assert len(empty_dir.subdirectories) == 1
        assert "added_dir" in empty_dir.subdirectories.keys()

        duplicate_dir = Directory("added_dir")
        duplicate_file = DigitalFile("added_dir")
        # Items with names already in the directory should be rejected
        # in this case, even files
        with pytest.raises(KeyError):
            empty_dir.add_subdirectory(duplicate_dir)
            empty_dir.add_file(duplicate_file)

    def test_add_file(self, empty_dir):
        file_to_add = DigitalFile("added_file")

        assert len(empty_dir.files) == 0
        empty_dir.add_file(file_to_add)
        assert len(empty_dir.files) == 1
        assert "added_file" in empty_dir.files.keys()

        duplicate_file = DigitalFile("added_file")
        duplicate_dir = Directory("added_file")
        # Items with names already in the directory should be rejected
        # in this case, even directories
        with pytest.raises(KeyError):
            empty_dir.add_file(duplicate_file)
            empty_dir.add_subdirectory(duplicate_dir)

    def test_get_item(self, populated_dir):
        result = populated_dir.get_item("test_subdir")
        assert isinstance(result, Directory)

        result = populated_dir.get_item("test_file")
        assert isinstance(result, DigitalFile)

        result = populated_dir.get_item("nonsense_key")
        assert result is None

    def test_directory_repr(self, empty_dir, populated_dir):
        expected_repr = "Directory(name='empty_dir_fixture', files=0, subdirectories=0)"
        assert repr(empty_dir) == expected_repr

        expected_repr = "Directory(name='populated_dir_fixture', files=2, subdirectories=1)"
        assert repr(populated_dir) == expected_repr

    def test_get_all_fortran_files(self, empty_dir):
        sub_dir = Directory("test_subdir")
        sub_dir.add_file(FortranFile("sub_file1"))
        sub_dir.add_file(FortranFile("sub_file2"))

        empty_dir.add_subdirectory(sub_dir)
        empty_dir.add_file(FortranFile("test_file1"))
        empty_dir.add_file(FortranFile("test_file2"))

        retrieved_files = empty_dir.get_all_fortran_files()
        assert len(retrieved_files) == 4
        assert isinstance(retrieved_files, list)

        retrieved_file_names = [file_obj.file_name for file_obj in retrieved_files]
        expected_file_names = ["sub_file1", "sub_file2", "test_file1", "test_file2"]

        for name in expected_file_names:
            assert name in retrieved_file_names
