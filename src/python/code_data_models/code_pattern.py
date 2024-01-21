ALL_RETURN_TYPES = "|".join(
    [
        "CHARACTER",
        "COMPLEX",
        "DOUBLE[ \\t]+COMPLEX",  # This [ \\t]+ gives us the option of one or MORE spaces in our regex between words
        "DOUBLE[ \\t]+PRECISION",
        "INTEGER",
        "LOGICAL",
        "REAL",
    ]
)


class CodePattern:
    """The names of all the types of Fortran code blocks we want to parse in this project."""

    END = "END"
    FUNCTION = "FUNCTION"
    FUNCTION_END = "FUNCTION_END"
    INTERFACE = "INTERFACE"
    INTERFACE_END = "INTERFACE_END"
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

    FUNCTION = (  # This is one monstrous regex...
        rf"^([\w\W]*;)?\s*"
        rf"((RECURSIVE[ \t]+)?(({ALL_RETURN_TYPES})[ \t]+)?|(({ALL_RETURN_TYPES})[ \t]+)?(RECURSIVE[ \t]+)?)?"
        rf"FUNCTION[ \t]+\w+[ \t]*\([ \w\,]*\)([ \t]+RESULT[ \t]*\([ \w\,]*\))?"
        rf"\s*(;[\w\W]*)?(!.*)?$"
    )
    FUNCTION_END = r"^([\w\W]*;)?\s*END[ \t]*FUNCTION([ \t]+\w+)?\s*(;[\w\W]*)?(!.*)?$"
    INTERFACE = r"^([\w\W]*;)?\s*INTERFACE\s*(;[\w\W]*)?(!.*)?$"
    INTERFACE_END = r"^([\w\W]*;)?\s*END[ \t]*INTERFACE\s*(;[\w\W]*)?(!.*)?$"
    MODULE = r"^([\w\W]*;)?\s*MODULE[ \t]+\w+\s*(;[\w\W]*)?(!.*)?$"
    MODULE_END = r"^([\w\W]*;)?\s*END([ \t]*MODULE([ \t]+\w+)?)?\s*(;[\w\W]*)?(!.*)?$"
    PROGRAM = r"^([\w\W]*;)?\s*PROGRAM[ \t]+\w+\s*(;[\w\W]*)?(!.*)?$"
    PROGRAM_END = r"^([\w\W]*;)?\s*END([ \t]*PROGRAM([ \t]+\w+)?)?\s*(;[\w\W]*)?(!.*)?$"
    SUBROUTINE = r"^([\w\W]*;)?\s*(RECURSIVE[ \t]+)?SUBROUTINE[ \t]+\w+[ \t]*\([ \w\,]*\)\s*(;[\w\W]*)?(!.*)?$"
    SUBROUTINE_END = r"^([\w\W]*;)?\s*END[ \t]*SUBROUTINE([ \t]+\w+)?\s*(;[\w\W]*)?(!.*)?$"
    TYPE = r"^([\w\W]*;)?\s*TYPE[ \t]+\w+\s*(;[\w\W]*)?(!.*)?$"
    TYPE_END = r"^([\w\W]*;)?\s*END[ \t]*TYPE([ \t]+\w+)?\s*(;[\w\W]*)?(!.*)?$"
