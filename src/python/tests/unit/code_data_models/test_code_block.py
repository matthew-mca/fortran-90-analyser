import pytest

from code_data_models.code_block import CodeBlock
from code_data_models.code_statement import CodeStatement
from code_data_models.fortran_function import FortranFunction
from code_data_models.fortran_interface import FortranInterface
from code_data_models.fortran_module import FortranModule
from code_data_models.fortran_program import FortranProgram
from code_data_models.fortran_subroutine import FortranSubroutine
from code_data_models.fortran_type import FortranType


class TestCodeBlock:
    @pytest.fixture
    def child_block_types(self):
        return [
            FortranFunction,
            FortranInterface,
            FortranModule,
            FortranProgram,
            FortranSubroutine,
            FortranType,
        ]

    @pytest.fixture
    def three_line_unit(self):
        return [
            CodeStatement(1, "line_1"),
            CodeStatement(2, "line_2"),
            CodeStatement(3, "line_3"),
        ]

    @pytest.fixture
    def one_line_unit(self):
        return [
            CodeStatement(1, "line_1"),
            CodeStatement(1, "line_2"),
            CodeStatement(1, "line_3"),
        ]

    def test_code_block_abstract_class(self):
        with pytest.raises(TypeError):
            test_code_block = CodeBlock([])  # noqa: F841

    @pytest.mark.skip(reason="Code block has been refactored")
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

    @pytest.mark.skip(reason="Code block has been refactored")
    def test_child_class_reprs(self, child_block_types, one_line_unit, three_line_unit):
        for block_type in child_block_types:
            block_object = block_type([])
            class_name = type(block_object).__name__
            expected_repr = f"{class_name}(lines_of_code=0)"
            assert repr(block_object) == expected_repr

            block_object = block_type(one_line_unit)
            expected_repr = f"{class_name}(lines_of_code=1)"
            assert repr(block_object) == expected_repr

            block_object = block_type(three_line_unit)
            expected_repr = f"{class_name}(lines_of_code=3)"
            assert repr(block_object) == expected_repr

    @pytest.mark.skip(reason="Code block has been refactored")
    def test_child_class_init(self, child_block_types):
        for block_type in child_block_types:
            # This init should fail
            with pytest.raises(TypeError):
                block_object = block_type()

            # This init should NOT fail
            block_object = block_type([])
            assert hasattr(block_object, "contents")
