import pytest

from code_data_models.code_block import CodeBlock
from code_data_models.fortran_do_loop import FortranDoLoop
from code_data_models.fortran_function import FortranFunction
from code_data_models.fortran_if_block import FortranIfBlock
from code_data_models.fortran_type import FortranType
from tests.object_factory import (
    random_code_statement,
    random_fortran_do_loop,
    random_fortran_function,
    random_fortran_if_block,
    random_fortran_interface,
    random_fortran_module,
    random_fortran_program,
    random_fortran_subroutine,
    random_fortran_type,
    random_variable,
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

    @pytest.mark.parametrize(
        "split_string,delimiter,expected_result",
        [
            (
                "*a*string*to*'be*split*with'*quotes*",
                "*",
                ["", "a", "string", "to", "'be*split*with'", "quotes", ""],
            ),
            (
                "'::'CHARACTER(LEN=1024) :: char_1=':: Declare :: variables with ::'",
                "::",
                ["'::'CHARACTER(LEN=1024) ", " char_1=':: Declare :: variables with ::'"],
            ),
            (
                "test!*!string!*!to!*!split!*!",
                "!*!",
                ["test", "string", "to", "split", ""],
            ),
        ],
    )
    def test_split_outside_quotes(self, split_string, delimiter, expected_result):
        code_block = random_fortran_program()
        split_result = code_block._split_outside_quotes(split_string, delimiter)

        assert split_result == expected_result

    def test_get_variables_not_in_subprograms(self):
        fake_file_path = "fake/dir/file.f90"

        test_program = random_fortran_program(
            parent_file_path=fake_file_path,
            subprograms=[],
        )

        test_var_1 = random_variable(
            data_type="INTEGER",
            attributes=[],
            name="variable_1",
            parent_file_path=fake_file_path,
            line_declared=1,
            is_array=False,
        )

        test_var_2 = random_variable(
            data_type="REAL",
            attributes=[],
            name="variable_2",
            parent_file_path=fake_file_path,
            line_declared=2,
            is_array=False,
        )

        test_var_3 = random_variable(
            data_type="COMPLEX",
            attributes=[],
            name="variable_3",
            parent_file_path=fake_file_path,
            line_declared=3,
            is_array=True,
        )

        test_var_4 = random_variable(
            data_type="DOUBLE PRECISION",
            attributes=[],
            name="variable_4",
            parent_file_path=fake_file_path,
            line_declared=4,
            is_array=False,
        )

        test_program.variables.extend(
            [
                test_var_1,
                test_var_2,
                test_var_3,
                test_var_4,
            ]
        )

        # As we create the subprogram that we will then add to the
        # existing program, the subprogram's two variables have been
        # created completely new, but with attributes identical to two
        # of the variables in the larger program. This is to prove the
        # comparison made is not based on two Variable objects being the
        # same object in memory.

        test_subprogram = random_fortran_function(
            parent_file_path=fake_file_path,
        )
        test_program.subprograms.append(test_subprogram)

        test_subprogram_var_1 = random_variable(
            data_type="INTEGER",
            attributes=[],
            name="variable_1",
            parent_file_path=fake_file_path,
            line_declared=1,
            is_array=False,
        )

        test_subprogram_var_2 = random_variable(
            data_type="REAL",
            attributes=[],
            name="variable_2",
            parent_file_path=fake_file_path,
            line_declared=2,
            is_array=False,
        )

        test_subprogram.variables.extend(
            [
                test_subprogram_var_1,
                test_subprogram_var_2,
            ]
        )

        non_subprogram_vars = test_program.get_variables_not_in_subprograms()
        assert len(non_subprogram_vars) == 2
        expected_names = [
            "variable_3",
            "variable_4",
        ]
        assert expected_names == [var.name for var in non_subprogram_vars]

    def test_get_variables_not_in_subprograms_type_error(self):
        unsupported_code_block = random_fortran_type()

        with pytest.raises(TypeError):
            unsupported_code_block.get_variables_not_in_subprograms()

    def test_get_all_subprograms(self):
        test_do_loop = random_fortran_do_loop()
        test_if_block = random_fortran_if_block()

        test_function = random_fortran_function(
            subprograms=[test_do_loop, test_if_block],
        )
        # Add an interface to check the function doesn't fall over when
        # one of the subprograms doesn't itself support subprograms
        test_interface = random_fortran_type()

        test_program = random_fortran_program(
            subprograms=[test_function, test_interface],
        )

        subprograms = test_program.get_all_subprograms()

        assert len(subprograms) == 4
        assert sum(isinstance(item, FortranDoLoop) for item in subprograms) == 1
        assert sum(isinstance(item, FortranFunction) for item in subprograms) == 1
        assert sum(isinstance(item, FortranIfBlock) for item in subprograms) == 1
        assert sum(isinstance(item, FortranType) for item in subprograms) == 1

    def test_get_all_subprograms_type_error(self):
        unsupported_code_block = random_fortran_type()

        with pytest.raises(TypeError):
            unsupported_code_block.get_all_subprograms()
