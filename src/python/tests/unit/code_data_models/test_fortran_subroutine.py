import pytest

from tests.object_factory import random_code_statement, random_fortran_subroutine


class TestFortranSubroutine:
    @pytest.mark.parametrize(
        "declaration,expected_result",
        [
            ("subroutine test_function()", "test_function"),
            ("RECURSIVE SUBROUTINE my_func()", "my_func"),
        ],
    )
    def test_find_block_name(self, declaration, expected_result):
        declaration_statement = random_code_statement(content=declaration)
        test_function = random_fortran_subroutine(contents=[declaration_statement])

        assert test_function.block_name == expected_result
