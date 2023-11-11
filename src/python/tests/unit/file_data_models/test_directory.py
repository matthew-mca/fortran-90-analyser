import pytest

from file_data_models import Directory, DigitalFile


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
            test_dir = Directory()

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
