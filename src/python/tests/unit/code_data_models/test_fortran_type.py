from tests.object_factory import random_code_statement, random_fortran_type


class TestFortranType:
    def test_find_block_name(self):
        declaration_statement = random_code_statement(content="TYPE my_derived_type")
        test_function = random_fortran_type(contents=[declaration_statement])

        assert test_function.block_name == "my_derived_type"
