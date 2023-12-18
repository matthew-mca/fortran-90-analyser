import pytest

from file_data_models.digital_file import DigitalFile


class TestDigitalFile:
    def test_digital_file_bad_init(self):
        with pytest.raises(TypeError):
            test_file = DigitalFile()  # noqa: F841

    def test_init_digital_file(self):
        test_file = DigitalFile("test_file")
        assert test_file.file_name == "test_file"
