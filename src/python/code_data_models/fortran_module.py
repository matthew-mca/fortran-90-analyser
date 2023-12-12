from typing import List

from .code_block import CodeBlock
from .code_line import CodeLine


class FortranModule(CodeBlock):
    """A Fortran 90 module.

    Attributes:
        contents: The lines of code that make up the module.
    """

    def __init__(self, contents: List[CodeLine]) -> None:
        """Initialises a module object."""

        super().__init__(contents)

    def get_snippet(self, start_index: int, end_index: int) -> List[CodeLine]:
        """See base class."""

        return super().get_snippet(start_index, end_index)
