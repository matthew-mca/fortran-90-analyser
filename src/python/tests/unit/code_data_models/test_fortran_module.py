from tests.object_factory import random_code_statement, random_fortran_module


class TestFortranModule:
    def test_find_block_name(self):
        declaration_statement = random_code_statement(content="MODULE test_module")
        test_function = random_fortran_module(contents=[declaration_statement])

        assert test_function.block_name == "test_module"
