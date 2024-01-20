from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranInterface(CodeBlock):
    """A Fortran 90 interface.

    Attributes:
        contents: The lines of code that make up the interface.
    """

    def __init__(self, contents: List[CodeStatement]) -> None:
        """Initialises an interface object."""

        super().__init__(contents)
