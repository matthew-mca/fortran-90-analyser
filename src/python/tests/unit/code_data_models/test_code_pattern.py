import re

import pytest

from code_data_models.code_pattern import CodePatternRegex


class TestCodePatternRegex:
    def assert_regex_result(self, pattern, string, expect_match):
        search_pattern = re.compile(pattern, re.IGNORECASE)
        result = search_pattern.match(string)

        if expect_match:
            assert result is not None
        else:
            assert result is None

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("MODULE test_module", True),
            ("test_module", False),
            ("Module", False),
            ("    MODULE    test_module   ", True),
            ("\t MoDulE test_module", True),
            ("Bad MODULE test_module statement", False),
            ("test command;  MODULE test_module; test command", True),
            ("MODULE\ntest_module", False),
            ("MODULE test_module ! comment", True),
        ],
    )
    def test_module_start(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.MODULE, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("end", True),
            ("\tEND", True),
            ("enD   MODULE  ", True),
            ("rend module", False),
            ("   END MODULE test_module  ", True),
            ("endmodule test_module", True),
            ("endmoduletest_module", False),
            ("endmodule", True),
            ("end test_module", False),
            ("do not end module test_module", False),
            ("test_module", False),
            ("MODULE; test_module", False),
            ("test command;  END MODULE test_module; test command", True),
            ("END\nMODULE\ntest_module", False),
            ("END MODULE test_module   !!  comment", True),
        ],
    )
    def test_module_end(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.MODULE_END, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("PROGRAM test_program", True),
            ("program test_program\n", True),
            ("    program   test_program   ", True),
            ("program", False),
            ("test_program", False),
            ("PROGRAM\ntest_program", False),
            ("PROGRAM test_program;   END", True),
            ("PROGRAM; test_program", False),
            ("test command;  PROGRAM test_program; test command", True),
            ("test command\nPROGRAM test_program", False),
            # The above case is likely valid from the POV of the compiler,
            # but given our parsing logic we shouldn't end up encountering it.
            ("PROGRAM test_program ! comment  ", True),
        ],
    )
    def test_program_start(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.PROGRAM, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("end", True),
            ("\tend", True),
            ("END    ", True),
            ("EnD", True),
            ("end program", True),
            ("END PROGRAM", True),
            ("end program test_program    ", True),
            ("END   PROGRAM   test_program", True),
            ("bend", False),
            ("   end", True),
            ("endprogram", True),
            ("ENDPROGRAMtest_program", False),
            ("ENDPROGRAM test_program", True),
            ("bad end", False),
            ("END test_program\n", False),
            ("test command;  END PROGRAM test_program; test command", True),
            ("END\nPROGRAM\ntest_program", False),
            ("END PROGRAM test_program !! comment", True),
        ],
    )
    def test_program_end(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.PROGRAM_END, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("type test_type", True),
            ("TYPE test_type", True),
            ("\t TYPE  ", False),
            ("  my_type   ", False),
            ("TYPE name with spaces", False),
            ("test command;  TYPE test_type; test command", True),
            ("TYPE\ntest_type", False),
            ("TYPE test_type !! comment", True),
        ],
    )
    def test_type_start(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.TYPE, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("END", False),
            ("END type", True),
            ("END TYPE", True),
            ("END TYPE test_type", True),
            ("END test_type", False),
            ("TYPE test_type", False),
            ("ENDTYPE", True),
            ("SEND TYPE test_type", False),
            ("ENDTYPEtest_type", False),
            ("test command;  END type test_type; test command", True),
            ("END\nTYPE\ntest_type", False),
            ("END TYPE test_type ! comment", True),
        ],
    )
    def test_type_end(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.TYPE_END, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("END", False),
            ("END function", True),
            ("END FUNCTION", True),
            ("END FUNCTION test_function", True),
            ("END test_function", False),
            ("FUNCTION test_function", False),
            ("ENDFUNCTION", True),
            ("SEND FUNCTION test_function", False),
            ("ENDFUNCTIONtestfunction", False),
            ("test command;  END function test_function; test command", True),
            ("END\nFUNCTION\ntest_function", False),
            ("END FUNCTION ! comment", True),
        ],
    )
    def test_function_end(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.FUNCTION_END, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("END", False),
            ("END subroutine", True),
            ("END SUBROUTINE", True),
            ("END SUBROUTINE test_subroutine", True),
            ("END test_subroutine", False),
            ("SUBROUTINE test_subroutine", False),
            ("ENDSUBROUTINE", True),
            ("SEND SUBROUTINE test_subroutine", False),
            ("ENDSUBROUTINEtestsubroutine", False),
            ("test command;  END subroutine test_subroutine; test command", True),
            ("END\nSUBROUTINE\ntest_subroutine", False),
            ("END SUBROUTINE ! comment ", True),
        ],
    )
    def test_subroutine_end(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.SUBROUTINE_END, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("REAL FUNCTION MY_TEST_FUNCTION(test_arg1, TEST_ARG2,TEST_ARG3)", True),
            ("COMPLEX     FUNCTION     MY_TEST_FUNCTION()", True),
            ("INTEGER FUNCTION MY_TEST_FUNCTION", False),
            ("test command; LOGICAL FUNCTION TEST_FUNCTION(ARG_1, ARG_2); test command", True),
            ("DOUBLE    PRECISION    FUNCTION TEST_FUNCTION(ARG)", True),
            ("FUNCTION test_function (arg_1, arg_2)", True),
            ("REAL\nFUNCTION\nTEST_FUNCTION()", False),
            ("DOUBLE COMPLEX FUNCTION()", False),
            ("function test_function (arg_1, arg_2) result(result_var)", True),
            ("COMPLEX FUNCTION MY_TEST_FUNCTION() ! comment", True),
            ("RECURSIVE FUNCTION TEST_RECURSION(test_arg) RESULT(result_var)", True),
            ("INTEGER RECURSIVE FUNCTION test_function(arg_1)", True),
            ("COMPLEX RECURSIVE FUNCTION test_function(test_arg) RESULT(result_var) ! comment", True),
        ],
    )
    def test_function_start(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.FUNCTION, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("SUBROUTINE TEST_SUBROUTINE (test_arg1, TEST_ARG2,TEST_ARG3)", True),
            ("SUBROUTINE     test_subroutine()", True),
            ("SUBROUTINE TEST_SUBROUTINE", False),
            ("test command; SUBROUTINE TEST_SUBROUTINE(ARG_1, ARG_2); test command", True),
            ("SUBROUTINE TEST_SUBROUTINE", False),
            ("INTEGER SUBROUTINE TEST_SUBROUTINE(ARG_1, ARG_2)", False),
            ("SUBROUTINE\nTEST_SUBROUTINE()", False),
            ("SUBROUTINE ()", False),
            ("SUBROUTINE TEST_SUBROUTINE() ! comment", True),
            ("RECURSIVE SUBROUTINE test_subroutine(arg_1)", True),
        ],
    )
    def test_subroutine_start(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.SUBROUTINE, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("  INTERFACE   ", True),
            ("test command; INTERFACE; test command", True),
            ("INTERFACE test_interface", False),
            ("NEW INTERFACE", False),
            ("INTERFACE ! comment", True),
        ],
    )
    def test_interface_start(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.INTERFACE, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("END INTERFACE", True),
            ("END INTERFACE test_inferface", False),
            ("SEND INTERFACE", False),
            ("end       INTERFACE", True),
            ("test command; END INTERFACE; test command", True),
            ("END INTERFACE ! comment  ", True),
        ],
    )
    def test_interface_end(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.INTERFACE_END, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("real, intent(in) :: test_real1, test_real2", True),
            ("Complex , intent(inout) :: test_complex", True),
            ("DOUBLE   PRECISION, INTENT(OUT) :: var_double = 3.45", True),
            ("CHARACTER :: test_int", True),
            ("LOGICAL test_log", False),
            ("type(test_type) :: type_object", True),
            ("INTEGER :: daysinyear=365, monthsinyear=12, weeksinyear=52", True),
            ("CHARACTER :: test_string='hello world'", True),
            ("DOUBLE COMPLEX :: this_variable_name_exceeds_31_characters", False),
            ("CHARACTER(LEN=1)  :: letter, digit", True),
            ("CHARACTER(1)      :: letter, digit", True),
            ("CHARACTER         :: letter, digit", True),
            ("CHARACTER(LEN=10) :: City, Nation*20, BOX, bug*1", True),
            ("CHARACTER(LEN=*) :: Title, Position", True),
            ("integer(i8), dimension(n) :: f", True),
            ("integer, dimension(5) :: array", True),
            ("real :: array(5)", True),
        ],
    )
    def test_variable_declaration(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.VARIABLE_DECLARATION, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("IF (condition) THEN", True),
            ("IF (condition) THEN    ! comment", True),
            ("IF ( X .LT. 0.0 ) THEN ", True),
            ("IF condition THEN", False),
            ("IF (condition)", False),
            ("test command; IF (condition) THEN; test command;", True),
        ],
    )
    def test_if_block(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.IF_BLOCK, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("END IF", True),
            ("END IF if_statement", False),
            ("SEND IF", False),
            ("end       IF", True),
            ("test command; END IF; test command", True),
            ("END IF ! comment  ", True),
            ("ENDIF", True),
            ("END", False),
        ],
    )
    def test_if_block_end(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.IF_BLOCK_END, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("DO WHILE (condition)", True),
            ("DO i = start, end, step", True),
            ("DO i = start, end", True),
            ("while (condition) do", True),
            ("DO 210 I = 1, 10", True),
        ],
    )
    def test_do_loop(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.DO_LOOP, string, expect_match)

    @pytest.mark.parametrize(
        "string,expect_match",
        [
            ("END DO", True),
            ("END", False),
            ("END DO do_loop", False),
            ("SEND DO", False),
            ("end       DO", True),
            ("test command; END DO; test command", True),
            ("END DO ! comment  ", True),
            ("ENDDO", True),
        ],
    )
    def test_do_loop_end(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.DO_LOOP_END, string, expect_match)
