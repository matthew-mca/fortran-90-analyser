class CodePattern:
    """The names of all the types of Fortran code blocks we want to parse in this project."""

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
    """The regex patterns for all the types of Fortran code blocks we want to parse in this project."""

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
