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

    DO_LOOP = (
        r"^\s*" r"(DO[ \t]*WHILE[ \t]*\(.*\)|WHILE[ \t]*\(.*\)[ \t]*DO|DO([ \t]+\d*)?[ \t]+\w+[ \t]+=.+)" r"\s*(!.*)?$"
    )
    DO_LOOP_END = r"^\s*END[ \t]*DO\s*(!.*)?$"
    FUNCTION = (  # This is one monstrous regex...
        rf"^\s*"
        rf"((RECURSIVE[ \t]+)?(({ALL_RETURN_TYPES})[ \t]+)?|(({ALL_RETURN_TYPES})[ \t]+)?(RECURSIVE[ \t]+)?)?"
        rf"FUNCTION[ \t]+\w+[ \t]*\([ \w\,]*\)([ \t]+RESULT[ \t]*\([ \w\,]*\))?"
        rf"\s*(!.*)?$"
    )
    FUNCTION_END = r"^\s*END[ \t]*FUNCTION([ \t]+\w+)?\s*(!.*)?$"
    IF_BLOCK = r"^\s*IF[ \t]*\(.*\)[ \t]*THEN\s*(!.*)?$"
    IF_BLOCK_END = r"^\s*END[ \t]*IF\s*(!.*)?$"
    INTERFACE = r"^\s*INTERFACE\s*(!.*)?$"
    INTERFACE_END = r"^\s*END[ \t]*INTERFACE\s*(!.*)?$"
    MODULE = r"^\s*MODULE[ \t]+\w+\s*(!.*)?$"
    MODULE_END = r"^\s*END([ \t]*MODULE([ \t]+\w+)?)?\s*(!.*)?$"
    PROGRAM = r"^\s*PROGRAM[ \t]+\w+\s*(!.*)?$"
    PROGRAM_END = r"^\s*END([ \t]*PROGRAM([ \t]+\w+)?)?\s*(!.*)?$"
    SUBROUTINE = r"^\s*(RECURSIVE[ \t]+)?SUBROUTINE[ \t]+\w+[ \t]*\([ \w\,]*\)\s*(!.*)?$"
    SUBROUTINE_END = r"^\s*END[ \t]*SUBROUTINE([ \t]+\w+)?\s*(!.*)?$"
    TYPE = r"^\s*TYPE[ \t]+\w+\s*(!.*)?$"
    TYPE_END = r"^\s*END[ \t]*TYPE([ \t]+\w+)?\s*(!.*)?$"
    VARIABLE_DECLARATION = (
        rf"^\s*"
        rf"({ALL_RETURN_TYPES}|TYPE\(.*\)).*::\s*\w{{1,31}}(\(\d+\))?(\*\d+)?(\s*=.*)?"
        rf"(,\s*\w{{1,31}}(\(\d+\))?(\*\d+)?(\s*=.*)?)*"
        rf"\s*(!.*)?$"
    )
