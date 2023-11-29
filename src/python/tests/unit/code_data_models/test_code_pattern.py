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
        ],
    )
    def test_type_end(self, string, expect_match):
        self.assert_regex_result(CodePatternRegex.TYPE_END, string, expect_match)
