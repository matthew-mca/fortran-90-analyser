import pytest

from code_data_models.fortran_program import FortranProgram


class TestFortranProgram:
    @pytest.fixture
    def empty_fortran_program(self):
        return FortranProgram([])

    def test_fortran_program_bad_init(self):
        with pytest.raises(TypeError):
            test_fortran_program = FortranProgram()  # noqa: F841

    def test_init_fortran_program(self, empty_fortran_program):
        assert hasattr(empty_fortran_program, "contents")

    def test_fortran_program_repr(self, empty_fortran_program):
        expected_repr = "FortranProgram(lines_of_code=0)"
        assert repr(empty_fortran_program) == expected_repr
