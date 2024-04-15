import re
from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranType(CodeBlock):
    """A 'derived type' in Fortran 90.

    Attributes:
        parent_file_path: The path to the Fortran 90 file the type is
          in.
        contents: The lines of code that make up the type.
        block_name: The name given to the type.
        variables: A list of all the variables declared as
          attributes in the type.
    """

    def __init__(self, parent_file_path: str, contents: List[CodeStatement]) -> None:
        """Initialises a type object."""

        super().__init__(parent_file_path, contents)
        self.block_name = self._find_block_name("TYPE")
        self.variables = self._find_variable_declarations()

    def _find_block_name(self, block_type: str) -> str:
        """Parses the code block's name from its declaration.

        This function adds to the base functionality of the
        '_find_block_name' function in the CodeBlock class, as there are
        multiple elements that need to be found and removed from a
        type declaration in order to retrieve its name.
        """

        start_line = super()._find_block_name(block_type)

        start_line = re.sub(".*::", "", start_line)

        return start_line.strip()
