import pytest

from tests.object_factory import random_code_statement, random_fortran_function


class TestFortranFunction:
    @pytest.mark.parametrize(
        "declaration,expected_result",
        [
            ("function test_function()", "test_function"),
            ("RECURSIVE FUNCTION my_func()", "my_func"),
            ("INTEGER FUNCTION random_name() result (value)", "random_name"),
            ("RECURSIVE COMPLEX FUNCTION hello(arg_1, arg_2)", "hello"),
        ],
    )
    def test_find_block_name(self, declaration, expected_result):
        declaration_statement = random_code_statement(content=declaration)
        test_function = random_fortran_function(contents=[declaration_statement])

        assert test_function.block_name == expected_result
