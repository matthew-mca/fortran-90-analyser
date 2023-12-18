import pytest

from code_data_models.fortran_module import FortranModule


class TestFortranModule:
    def test_fortran_module_bad_init(self):
        with pytest.raises(TypeError):
            test_fortran_module = FortranModule()  # noqa: F841

    def test_init_fortran_module(self):
        test_fortran_module = FortranModule([])
        assert hasattr(test_fortran_module, "contents")
