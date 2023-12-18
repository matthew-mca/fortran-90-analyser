import pytest

from code_data_models.fortran_type import FortranType


class TestFortranType:
    def test_fortran_type_bad_init(self):
        with pytest.raises(TypeError):
            test_fortran_type = FortranType()  # noqa: F841

    def test_init_fortran_type(self):
        test_fortran_type = FortranType([])
        assert hasattr(test_fortran_type, "contents")
