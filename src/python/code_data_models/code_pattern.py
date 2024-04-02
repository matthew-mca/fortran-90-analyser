from code_data_models.variable import Variable

# Replacing the whitespaces in the Fortran data types with [ \\t]+
# gives us the option of one or MORE spaces in our regex between words
ALL_RETURN_TYPES = "|".join([data_type.replace(" ", "[ \\t]+") for data_type in Variable.ALL_DATA_TYPES])


class CodePattern:
    """The names of types of Fortran code blocks."""

    DO_LOOP = "DO_LOOP"
    DO_LOOP_END = "DO_LOOP_END"
    END = "END"
    FUNCTION = "FUNCTION"
    FUNCTION_END = "FUNCTION_END"
    IF_BLOCK = "IF_BLOCK"
    IF_BLOCK_END = "IF_BLOCK_END"
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
    """The regex patterns for types of Fortran code blocks."""

    # These used to be required pieces of every pattern until the
    # addition of logic that now splits lines with semicolons into
    # distinct commands during parsing. Who knows, maybe these may get
    # used again some day, so going to leave them here...
    _SEMICOLON_BEFORE = r"([\w\W]*;)?"
    _SEMICOLON_AFTER = r"(;[\w\W]*)?"

    DO_LOOP = r"^\s*(\d+\s+)?(DO\s*WHILE\s*\(.*\)|WHILE\s*\(.*\)\s*DO|DO((\s+\d*)?\s+\w+\s*=.+)?)\s*(!.*)?$"
    DO_LOOP_END = r"^\s*(\d+\s+)?END\s*DO\s*(!.*)?$"
    FUNCTION = (
        rf"^\s*(.*\s*)((RECURSIVE\s+)?(({ALL_RETURN_TYPES})\s+)?|(({ALL_RETURN_TYPES})\s+)?(RECURSIVE\s+)?)?"
        rf"FUNCTION\s+\w+\s*\([ \w\,]*\)(\s+RESULT\s*\([ \w\,]*\))?\s*(!.*)?$"
    )
    FUNCTION_END = r"^\s*END\s*FUNCTION(\s+\w+)?\s*(!.*)?$"
    IF_BLOCK = r"^\s*(\d+\s+)?IF\s*\(.*\)\s*THEN\s*(!.*)?$"
    IF_BLOCK_END = r"^\s*END\s*IF\s*(!.*)?$"
    INTERFACE = r"^\s*(ABSTRACT\s+)?INTERFACE(\s+\w+)?\s*(!.*)?$"
    INTERFACE_END = r"^\s*END\s*INTERFACE(\s+\w+)?\s*(!.*)?$"
    MODULE = r"^\s*MODULE\s+\w+\s*(!.*)?$"
    MODULE_END = r"^\s*END(\s*MODULE(\s+\w+)?)?\s*(!.*)?$"
    PROGRAM = r"^\s*PROGRAM\s+\w+\s*(!.*)?$"
    PROGRAM_END = r"^\s*END(\s*PROGRAM(\s+\w+)?)?\s*(!.*)?$"
    SUBROUTINE = r"^\s*(RECURSIVE\s+)?SUBROUTINE\s+\w+\s*(\([ \w\,]*\))?\s*(!.*)?$"
    SUBROUTINE_END = r"^\s*END\s*SUBROUTINE(\s+\w+)?\s*(!.*)?$"
    TYPE = r"^\s*TYPE(\s*,.*)?(\s*::\s*)?\s+\w+\s*(!.*)?$"
    TYPE_END = r"^\s*END\s*TYPE(\s+\w+)?\s*(!.*)?$"
    VARIABLE_DECLARATION = (
        rf"^\s*({ALL_RETURN_TYPES}|TYPE\(.*\)).*::\s*\w{{1,31}}(\(\d+\))?(\*\d+)?(\s*=.*)?"
        rf"(,\s*\w{{1,31}}(\(\d+\))?(\*\d+)?(\s*=.*)?)*\s*(!.*)?$"
    )
