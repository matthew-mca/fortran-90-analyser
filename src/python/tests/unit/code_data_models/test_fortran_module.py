import pytest

from code_data_models.fortran_module import FortranModule


class TestFortranModule:
    @pytest.fixture
    def empty_fortran_module(self):
        return FortranModule([])

    def test_fortran_module_bad_init(self):
        with pytest.raises(TypeError):
            test_fortran_module = FortranModule()  # noqa: F841

    def test_init_fortran_module(self, empty_fortran_module):
        assert hasattr(empty_fortran_module, "contents")

    def test_fortran_module_repr(self, empty_fortran_module):
        expected_repr = "FortranModule(lines_of_code=0)"
        assert repr(empty_fortran_module) == expected_repr
