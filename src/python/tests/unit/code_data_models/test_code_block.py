import pytest

from code_data_models.code_block import CodeBlock
from tests.object_factory import (
    random_code_statement,
    random_fortran_function,
    random_fortran_interface,
    random_fortran_module,
    random_fortran_program,
    random_fortran_subroutine,
    random_fortran_type,
)


class TestCodeBlock:
    @pytest.fixture
    def child_block_types(self):
        return [
            random_fortran_function(),
            random_fortran_interface(),
            random_fortran_module(),
            random_fortran_program(),
            random_fortran_subroutine(),
            random_fortran_type(),
        ]

    def test_code_block_abstract_class(self):
        with pytest.raises(TypeError):
            test_code_block = CodeBlock([])  # noqa: F841

    def test_code_block_len(self, child_block_types):
        for block_object in child_block_types:
            start_line_number = block_object.start_line_number
            end_line_number = block_object.end_line_number
            expected_line_number = (end_line_number - start_line_number) + 1

            assert len(block_object) == expected_line_number

    def test_child_class_reprs(self, child_block_types):
        for block_object in child_block_types:
            expected_class_name = type(block_object).__name__
            expected_lines_of_code = len(block_object)
            expected_repr = f"{expected_class_name}(lines_of_code={expected_lines_of_code})"
            assert repr(block_object) == expected_repr

    def test_contains_block(self):
        line_1 = random_code_statement(line_number=1)
        line_25 = random_code_statement(line_number=25)
        line_50 = random_code_statement(line_number=50)
        line_100 = random_code_statement(line_number=100)

        file_path_1 = "path/file_1"
        file_path_2 = "path/file_2"

        # Case 1 - separate files
        file_1_block = random_fortran_program(parent_file_path=file_path_1)
        file_2_block = random_fortran_program(parent_file_path=file_path_2)

        assert not file_1_block.contains_block(file_2_block)

        # Case 2 - block 1 contains block 2
        containing_block = random_fortran_program(parent_file_path=file_path_1, contents=[line_1, line_100])
        contained_block = random_fortran_subroutine(parent_file_path=file_path_1, contents=[line_25, line_50])

        assert containing_block.contains_block(contained_block)

        # Case 3 - blocks with line numbers outside and EQUAL TO block
        # 1's should not be considered as contained
        block_1 = random_fortran_program(parent_file_path=file_path_1, contents=[line_25, line_50])
        block_2 = random_fortran_module(parent_file_path=file_path_1, contents=[line_25, line_50])

        assert not block_1.contains_block(block_2)

        block_2 = random_fortran_module(parent_file_path=file_path_1, contents=[line_1, line_100])

        assert not block_1.contains_block(block_2)

    def test_find_variable_declarations(self):
        declaration_1 = random_code_statement(content="COMPLEX :: comp_1, comp_2")
        declaration_2 = random_code_statement(content="integer, pointer :: int_point")
        declaration_3 = random_code_statement(content="character(len=1024), INTENT(IN) :: char_1='Hello', char_2")
        variable_usage_statement = random_code_statement(content="char_2=char_1")

        block_with_declarations = random_fortran_module(
            contents=[
                declaration_1,
                declaration_2,
                declaration_3,
                variable_usage_statement,
            ]
        )
        found_variables = block_with_declarations.variables

        assert len(found_variables) == 5

        data_types = [variable.data_type for variable in found_variables]

        assert data_types.count("COMPLEX") == 2
        assert data_types.count("INTEGER") == 1
        assert data_types.count("CHARACTER(LEN=1024)") == 2

        expected_names = ["comp_1", "comp_2", "int_point", "char_1", "char_2"]
        variable_names = [variable.name for variable in found_variables]

        for name in expected_names:
            assert name in variable_names

        variables_marked_unused = [variable.name for variable in found_variables if variable.possibly_unused]
        expected_names = ["comp_1", "comp_2", "int_point"]

        # Due to the "variable_usage_statement", char_1 and char_2 will
        # not be considered as possibly unused
        assert "char_1" not in variables_marked_unused
        assert "char_2" not in variables_marked_unused
        for name in expected_names:
            assert name in variables_marked_unused
