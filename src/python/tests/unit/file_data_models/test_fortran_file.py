import pytest

from code_data_models.code_line import CodeLine
from code_data_models.code_pattern import CodePattern
from code_data_models.fortran_program import FortranProgram
from file_data_models.fortran_file import FortranFile


class TestFortranFile:
    @pytest.fixture
    def fortran_hello_world(self):
        return [
            "PROGRAM test_program",
            "Print *, 'Hello World'",
            "END PROGRAM test_program",
        ]

    @pytest.fixture
    def hello_world_file(self, fortran_hello_world):
        test_f90_file = FortranFile("hello_world_file", fortran_hello_world)
        return test_f90_file

    def test_fortran_file_bad_init(self):
        with pytest.raises(TypeError):
            test_f90_file = FortranFile()

    def test_init_fortran_file(self):
        test_f90_file = FortranFile("test_file")
        assert test_f90_file.file_name == "test_file"

    def test_init_fortran_file_with_code(self, fortran_hello_world):
        test_f90_file = FortranFile("test_file", fortran_hello_world)
        file_contents = test_f90_file.contents

        assert len(file_contents) == 3
        for line in file_contents:
            assert isinstance(line, CodeLine)

        assert CodePattern.PROGRAM in file_contents[0].matched_patterns
        assert CodePattern.PROGRAM_END in file_contents[2].matched_patterns

    def test_tag_lines(self, hello_world_file):
        file_contents = hello_world_file.contents

        assert CodePattern.PROGRAM in file_contents[0].matched_patterns
        assert CodePattern.PROGRAM_END in file_contents[2].matched_patterns

    def test_parse_code_blocks(self, hello_world_file):
        assert len(hello_world_file.components) == 1
        assert isinstance(hello_world_file.components[0], FortranProgram)
