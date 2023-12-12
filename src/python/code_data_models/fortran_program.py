from typing import List

from .code_block import CodeBlock
from .code_line import CodeLine


class FortranProgram(CodeBlock):
    """A Fortran 90 program unit.

    Attributes:
        contents: The lines of code that make up the program.
    """

    def __init__(self, contents: List[CodeLine]) -> None:
        """Initialises a program object."""

        super().__init__(contents)

    def get_snippet(self, start_index: int, end_index: int) -> List[CodeLine]:
        """See base class."""

        return super().get_snippet(start_index, end_index)
