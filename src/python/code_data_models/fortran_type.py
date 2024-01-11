from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranType(CodeBlock):
    """A 'derived type' in Fortran 90.

    Attributes:
        contents: The lines of code that make up the type.
    """

    def __init__(self, contents: List[CodeStatement]) -> None:
        """Initialises a type object."""

        super().__init__(contents)
