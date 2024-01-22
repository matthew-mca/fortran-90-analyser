import pytest

from code_data_models.code_pattern import CodePattern
from code_data_models.code_statement import CodeStatement


class TestCodeStatement:
    @pytest.fixture
    def hello_world_line(self):
        return CodeStatement(1, "Print *, 'Hello World'")

    def test_code_statement_bad_init(self):
        with pytest.raises(TypeError):
            test_code_line = CodeStatement()  # noqa: F841

    def test_init_code_statement(self):
        line = "END PROGRAM test_program"
        test_code_statement = CodeStatement(22, line)

        assert test_code_statement.line_number == 22
        assert test_code_statement.content == line
        assert test_code_statement.matched_patterns == []

    def test_add_pattern(self, hello_world_line):
        hello_world_line.add_pattern(CodePattern.PROGRAM)

        assert hello_world_line.matched_patterns == [CodePattern.PROGRAM]

    def test_has_matched_patterns(self, hello_world_line):
        assert hello_world_line.has_matched_patterns() is False
        hello_world_line.add_pattern(CodePattern.PROGRAM)
        assert hello_world_line.has_matched_patterns() is True

    def test_is_end_statement(self, hello_world_line):
        assert hello_world_line.is_end_statement() is False

        hello_world_line.add_pattern(CodePattern.FUNCTION)
        assert hello_world_line.is_end_statement() is False

        hello_world_line.add_pattern(CodePattern.FUNCTION_END)
        assert hello_world_line.is_end_statement() is True

    def test_code_statement_repr(self, hello_world_line):
        expected_repr = "CodeStatement(line_number=1, content=\"Print *, 'Hello World'\")"
        assert repr(hello_world_line) == expected_repr
