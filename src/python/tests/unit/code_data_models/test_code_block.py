import pytest

from code_data_models.code_block import CodeBlock
from code_data_models.code_statement import CodeStatement
from code_data_models.fortran_program import FortranProgram


class TestCodeBlock:
    def test_code_block_abstract_class(self):
        with pytest.raises(TypeError):
            test_code_block = CodeBlock([])  # noqa: F841

    def test_code_block_len(self):
        empty_program = FortranProgram([])
        assert len(empty_program) == 0

        simple_program = FortranProgram(
            [
                CodeStatement(1, "PROGRAM test_program"),
                CodeStatement(2, "END PROGRAM test_program"),
            ]
        )
        assert len(simple_program) == 2
