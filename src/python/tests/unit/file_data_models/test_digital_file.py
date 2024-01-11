import pytest

from file_data_models.digital_file import DigitalFile


class TestDigitalFile:
    @pytest.fixture
    def test_file(self):
        return DigitalFile("test_file")

    def test_digital_file_bad_init(self):
        with pytest.raises(TypeError):
            test_file = DigitalFile()  # noqa: F841

    def test_init_digital_file(self, test_file):
        assert test_file.file_name == "test_file"

    def test_digital_file_repr(self, test_file):
        expected_repr = "DigitalFile(file_name='test_file')"
        assert repr(test_file) == expected_repr
