from tests.object_factory import random_code_statement, random_fortran_program


class TestFortranProgram:
    def test_find_block_name(self):
        declaration_statement = random_code_statement(content="PROGRAM test_program")
        test_function = random_fortran_program(contents=[declaration_statement])

        assert test_function.block_name == "test_program"
