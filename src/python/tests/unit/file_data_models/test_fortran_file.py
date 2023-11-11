import pytest

from file_data_models import FortranFile


class TestFortranFile:
    def test_fortran_file_bad_init(self):
        with pytest.raises(TypeError):
            test_f90_file = FortranFile()

    def test_init_fortran_file(self):
        test_f90_file = FortranFile("test_file")
        assert test_f90_file.file_name == "test_file"
