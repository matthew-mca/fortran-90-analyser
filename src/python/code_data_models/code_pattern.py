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


# TODO: With the line splitting logic now present in our parsing, are
# the start and end portions of each regex that allow for semicolons
# even needed anymore?
class CodePatternRegex:
    """The regex patterns for types of Fortran code blocks."""

    DO_LOOP = (
        r"^([\w\W]*;)?\s*"
        r"(DO[ \t]*WHILE[ \t]*\(.*\)|WHILE[ \t]*\(.*\)[ \t]*DO|DO([ \t]+\d*)?[ \t]+\w+[ \t]+=.+)"
        r"\s*(;[\w\W]*)?(!.*)?$"
    )
    DO_LOOP_END = r"^([\w\W]*;)?\s*END[ \t]*DO\s*(;[\w\W]*)?(!.*)?$"
    FUNCTION = (  # This is one monstrous regex...
        rf"^([\w\W]*;)?\s*"
        rf"((RECURSIVE[ \t]+)?(({ALL_RETURN_TYPES})[ \t]+)?|(({ALL_RETURN_TYPES})[ \t]+)?(RECURSIVE[ \t]+)?)?"
        rf"FUNCTION[ \t]+\w+[ \t]*\([ \w\,]*\)([ \t]+RESULT[ \t]*\([ \w\,]*\))?"
        rf"\s*(;[\w\W]*)?(!.*)?$"
    )
    FUNCTION_END = r"^([\w\W]*;)?\s*END[ \t]*FUNCTION([ \t]+\w+)?\s*(;[\w\W]*)?(!.*)?$"
    IF_BLOCK = r"^([\w\W]*;)?\s*IF[ \t]*\(.*\)[ \t]*THEN\s*(;[\w\W]*)?(!.*)?$"
    IF_BLOCK_END = r"^([\w\W]*;)?\s*END[ \t]*IF\s*(;[\w\W]*)?(!.*)?$"
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
    VARIABLE_DECLARATION = (
        rf"^([\w\W]*;)?\s*"
        rf"({ALL_RETURN_TYPES}|TYPE\(.*\)).*::\s*\w{{1,31}}(\(\d+\))?(\*\d+)?(\s*=.*)?"
        rf"(,\s*\w{{1,31}}(\(\d+\))?(\*\d+)?(\s*=.*)?)*"
        rf"\s*(;[\w\W]*)?(!.*)?$"
    )
