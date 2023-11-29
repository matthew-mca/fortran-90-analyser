"""
An enum that contains the code block names and regex patterns for various components of Fortran 90 code.

The second enum houses all the regular expressions that correspond to the different types of code blocks
that we aim to parse. This means that as more support is added for the different formatting of Fortran 90,
these patterns can just be directly edited rather than trying to adapt the parsing logic in multiple 
places.
"""


class CodePattern:
    COMMENT = "COMMENT"
    END = "END"
    FUNCTION = "FUNCTION"
    FUNCTION_END = "FUNCTION_END"
    MODULE = "MODULE"
    MODULE_END = "MODULE_END"
    PROGRAM = "PROGRAM"
    PROGRAM_END = "PROGRAM_END"
    SUBROUTINE = "SUBROUTINE"
    SUBROUTINE_END = "SUBROUTINE_END"
    TYPE = "TYPE"
    TYPE_END = "TYPE_END"


class CodePatternRegex:
    COMMENT = r""
    FUNCTION = r""
    FUNCTION_END = r""
    MODULE = r"^([\w\W]*;)?\s*MODULE[ \t]+\w+\s*(;[\w\W]*)?$"
    MODULE_END = r"^([\w\W]*;)?\s*END([ \t]*MODULE([ \t]+\w+)?)?\s*(;[\w\W]*)?$"
    PROGRAM = r"^([\w\W]*;)?\s*PROGRAM[ \t]+\w+\s*(;[\w\W]*)?$"
    PROGRAM_END = r"^([\w\W]*;)?\s*END([ \t]*PROGRAM([ \t]+\w+)?)?\s*(;[\w\W]*)?$"
    SUBROUTINE = r""
    SUBROUTINE_END = r""
    TYPE = r"^([\w\W]*;)?\s*TYPE[ \t]+\w+\s*(;[\w\W]*)?$"
    TYPE_END = r"^([\w\W]*;)?\s*END[ \t]*TYPE([ \t]+\w+)?\s*(;[\w\W]*)?$"
