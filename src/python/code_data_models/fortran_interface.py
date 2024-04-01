from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranInterface(CodeBlock):
    """A Fortran 90 interface.

    Attributes:
        parent_file_path: The path to the Fortran 90 file the interface
          is in.
        contents: The lines of code that make up the interface.
    """

    def __init__(self, parent_file_path: str, contents: List[CodeStatement]) -> None:
        """Initialises an interface object."""

        super().__init__(parent_file_path, contents)
        self.block_name = self._find_block_name("INTERFACE")
