import pytest

from code_data_models.fortran_program import FortranProgram


class TestFortranProgram:
    def test_fortran_program_bad_init(self):
        with pytest.raises(TypeError):
            test_fortran_program = FortranProgram()  # noqa: F841

    def test_init_fortran_program(self):
        test_fortran_program = FortranProgram([])
        assert hasattr(test_fortran_program, "contents")
