from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranProgram(CodeBlock):
    """A Fortran 90 program unit.

    Attributes:
        contents: The lines of code that make up the program.
    """

    def __init__(self, contents: List[CodeStatement]) -> None:
        """Initialises a program object."""

        super().__init__(contents)
