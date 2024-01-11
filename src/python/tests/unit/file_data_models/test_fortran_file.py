import pytest

from code_data_models.code_pattern import CodePattern
from code_data_models.code_statement import CodeStatement
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
    def fortran_with_semicolons(self):  # Same statements as the above fixture, but condensed to one line.
        return ["PROGRAM test_program; Print *, 'Hello World'; END PROGRAM test_program"]

    @pytest.fixture
    def empty_fortran_file(self):
        return FortranFile("empty_file")

    @pytest.fixture
    def hello_world_file(self, fortran_hello_world):
        test_f90_file = FortranFile("hello_world_file", fortran_hello_world)
        return test_f90_file

    @pytest.fixture
    def semicolon_file(self, fortran_with_semicolons):
        test_f90_file = FortranFile("semicolon_file", fortran_with_semicolons)
        return test_f90_file

    def test_fortran_file_bad_init(self):
        with pytest.raises(TypeError):
            test_f90_file = FortranFile()  # noqa: F841

    def test_init_fortran_file(self):
        test_f90_file = FortranFile("test_file")
        assert test_f90_file.file_name == "test_file"

    def test_init_fortran_file_with_code(self, hello_world_file, semicolon_file):
        assert len(hello_world_file) == 3
        file_contents = hello_world_file.contents
        assert len(file_contents) == 3
        for line in file_contents:
            assert isinstance(line, CodeStatement)

        assert CodePattern.PROGRAM in file_contents[0].matched_patterns
        assert CodePattern.PROGRAM_END in file_contents[2].matched_patterns

        # Despite the difference in the number of actual lines
        # in both versions of our hello world file, the length
        # of the contents list (i.e. the number of instructions)
        # should be the same.
        assert len(semicolon_file) == 1
        file_contents = semicolon_file.contents
        assert len(file_contents) == 3
        for line in file_contents:
            assert isinstance(line, CodeStatement)

        assert CodePattern.PROGRAM in file_contents[0].matched_patterns
        assert CodePattern.PROGRAM_END in file_contents[2].matched_patterns

    def test_tag_lines(self, hello_world_file):
        file_contents = hello_world_file.contents

        assert CodePattern.PROGRAM in file_contents[0].matched_patterns
        assert CodePattern.PROGRAM_END in file_contents[2].matched_patterns

    def test_parse_code_blocks(self, hello_world_file):
        assert len(hello_world_file.components) == 1
        assert isinstance(hello_world_file.components[0], FortranProgram)

    def test_fortran_file_repr(self, hello_world_file):
        expected_repr = "FortranFile(file_name='hello_world_file', lines_of_code=3, code_blocks=1)"
        assert repr(hello_world_file) == expected_repr

    def test_parse_statements_with_semicolons(self, fortran_with_semicolons):
        test_f90_file = FortranFile("semicolon_file", fortran_with_semicolons)
        assert len(test_f90_file.components) == 1

        parsed_component = test_f90_file.components[0]
        assert isinstance(parsed_component, FortranProgram)
        # Len is calculated using line numbers,
        # so it should differ from the actual length of contents here.
        assert len(parsed_component) == 1
        assert len(parsed_component.contents) == 3

    def test_get_snippet(self, empty_fortran_file, hello_world_file, semicolon_file):
        with pytest.raises(ValueError):
            snippet = empty_fortran_file.get_snippet(-1, 1)

        snippet = empty_fortran_file.get_snippet(1, 1)
        assert snippet == []

        snippet = hello_world_file.get_snippet(1, 1)
        assert len(snippet) == 1

        snippet = semicolon_file.get_snippet(1, 1)
        assert len(snippet) == 3

    def test_fortran_file_len(self, empty_fortran_file, hello_world_file, semicolon_file):
        assert len(empty_fortran_file) == 0
        assert len(hello_world_file) == 3
        assert len(semicolon_file) == 1
