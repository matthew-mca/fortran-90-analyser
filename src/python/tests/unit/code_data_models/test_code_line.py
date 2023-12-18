import pytest

from code_data_models.code_line import CodeLine
from code_data_models.code_pattern import CodePattern


class TestCodeLine:
    @pytest.fixture
    def hello_world_line(self):
        return CodeLine("Print *, 'Hello World'")

    def test_code_line_bad_init(self):
        with pytest.raises(TypeError):
            test_code_line = CodeLine()  # noqa: F841

    def test_init_code_line(self):
        line = "END PROGRAM test_program"
        test_code_line = CodeLine(line)

        assert test_code_line.line_content == line
        assert test_code_line.matched_patterns == []

    def test_add_pattern(self, hello_world_line):
        hello_world_line.add_pattern(CodePattern.COMMENT)

        assert hello_world_line.matched_patterns == [CodePattern.COMMENT]

    def test_has_matched_patterns(self, hello_world_line):
        assert hello_world_line.has_matched_patterns() is False
        hello_world_line.add_pattern(CodePattern.COMMENT)
        assert hello_world_line.has_matched_patterns() is True

    def test_contains_end_statement(self, hello_world_line):
        assert hello_world_line.contains_end_statement() is False

        hello_world_line.add_pattern(CodePattern.COMMENT)
        assert hello_world_line.contains_end_statement() is False

        hello_world_line.add_pattern(CodePattern.FUNCTION_END)
        assert hello_world_line.contains_end_statement() is True

    def test_code_line_repr(self, hello_world_line):
        hello_world_line.add_pattern(CodePattern.COMMENT)

        assert repr(hello_world_line) == "CodeLine(\"Print *, 'Hello World'\", ['COMMENT'])"
