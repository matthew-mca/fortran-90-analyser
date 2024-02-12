from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranProgram(CodeBlock):
    """A Fortran 90 program unit.

    Attributes:
        parent_file_path: The path to the Fortran 90 file the program
          is in.
        contents: The lines of code that make up the program.
        block_name: The name given to the program.
        variables: A list of all the variables in the program.
    """

    def __init__(self, parent_file_path: str, contents: List[CodeStatement]) -> None:
        """Initialises a program object."""

        super().__init__(parent_file_path, contents)
        self.block_name = self._find_block_name("PROGRAM")
        self.variables = self._find_variable_declarations()
