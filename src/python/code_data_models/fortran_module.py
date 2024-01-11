from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranModule(CodeBlock):
    """A Fortran 90 module.

    Attributes:
        contents: The lines of code that make up the module.
    """

    def __init__(self, contents: List[CodeStatement]) -> None:
        """Initialises a module object."""

        super().__init__(contents)
