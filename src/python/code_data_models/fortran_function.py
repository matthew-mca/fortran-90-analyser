import re
from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement
from .variable import Variable


class FortranFunction(CodeBlock):
    """A Fortran 90 function.

    Attributes:
        parent_file_path: The path to the Fortran 90 file the function
          is in.
        contents: The lines of code that make up the function.
        block_name: The name given to the function.
        variables: A list of all the variables in the function.
    """

    def __init__(self, parent_file_path: str, contents: List[CodeStatement]) -> None:
        """Initialises a function object."""

        super().__init__(parent_file_path, contents)
        self.block_name = self._find_block_name("FUNCTION")
        self.variables = self._find_variable_declarations()

    @property
    def is_recursive(self) -> bool:
        start_line = self.contents[0].content

        return re.search(r"\bRECURSIVE\b", start_line, re.IGNORECASE) is not None

    def _find_block_name(self, block_type: str) -> str:
        """Parses the code block's name from its declaration.

        This function adds to the base functionality of the
        '_find_block_name' function in the CodeBlock class, as there are
        multiple elements that need to be found and removed from a
        function declaration in order to retrieve its name.
        """

        # This call to super will remove the word 'function' for us,
        # but we are not done extracting the name yet.
        start_line = super()._find_block_name(block_type)

        # Remove potential use of the RECURSIVE keyword.
        start_line = re.sub(r"\bRECURSIVE\b", "", start_line, flags=re.IGNORECASE)

        # Remove stated return type of the function (if any).
        all_return_types = "|".join([data_type.replace(" ", "[ \\t]+") for data_type in Variable.ALL_DATA_TYPES])
        start_line = re.sub(rf"\b({all_return_types})\b", "", start_line, flags=re.IGNORECASE)

        # Remove anything from the first set of brackets onwards.
        start_line = re.sub(r"\(.*\).*", "", start_line, flags=re.IGNORECASE)

        return start_line.strip()
