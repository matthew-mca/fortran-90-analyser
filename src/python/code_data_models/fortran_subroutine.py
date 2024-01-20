from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranSubroutine(CodeBlock):
    """A Fortran 90 subroutine.

    Attributes:
        contents: The lines of code that make up the subroutine.
    """

    def __init__(self, contents: List[CodeStatement]) -> None:
        """Initialises a subroutine object."""

        super().__init__(contents)

    # TODO: Possible attribute for whether recursive or not?
