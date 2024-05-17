from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranDoLoop(CodeBlock):
    """A Fortran 90 DO loop.

    Attributes:
        parent_file_path: The path to the Fortran 90 file the DO loop is
          in.
        contents: The lines of code that make up the DO loop.
        variables: A list of all the variables in the DO loop.
        subprograms: A list of CodeBlock objects contained by the code
          block being instantiated.
    """

    def __init__(self, parent_file_path: str, contents: List[CodeStatement], subprograms: List[CodeBlock]) -> None:
        """Initialises a DO loop object."""

        super().__init__(parent_file_path, contents)
        self.variables = self._find_variable_declarations()
        self.subprograms = subprograms
