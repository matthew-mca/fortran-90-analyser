from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranType(CodeBlock):
    """A 'derived type' in Fortran 90.

    Attributes:
        parent_file_path: The path to the Fortran 90 file the type is
          in.
        contents: The lines of code that make up the type.
        block_name: The name given to the type.
        type_attributes: A list of all the variables declared as
          attributes in the type.
    """

    def __init__(self, parent_file_path: str, contents: List[CodeStatement]) -> None:
        """Initialises a type object."""

        super().__init__(parent_file_path, contents)
        self.block_name = self._find_block_name("TYPE")
        self.type_attributes = self._find_variable_declarations()
