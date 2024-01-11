import pytest

from code_data_models.fortran_type import FortranType


class TestFortranType:
    @pytest.fixture
    def empty_fortran_type(self):
        return FortranType([])

    def test_fortran_type_bad_init(self):
        with pytest.raises(TypeError):
            test_fortran_type = FortranType()  # noqa: F841

    def test_init_fortran_type(self, empty_fortran_type):
        assert hasattr(empty_fortran_type, "contents")

    def test_fortran_type_repr(self, empty_fortran_type):
        expected_repr = "FortranType(lines_of_code=0)"
        assert repr(empty_fortran_type) == expected_repr
