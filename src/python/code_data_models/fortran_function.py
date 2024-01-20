from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranFunction(CodeBlock):
    """A Fortran 90 function.

    Attributes:
        contents: The lines of code that make up the function.
    """

    def __init__(self, contents: List[CodeStatement]) -> None:
        """Initialises a function object."""

        super().__init__(contents)

    # TODO: Possible attribute for whether recursive or not?
