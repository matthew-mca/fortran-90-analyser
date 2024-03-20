from typing import List

from .code_block import CodeBlock
from .code_statement import CodeStatement


class FortranModule(CodeBlock):
    """A Fortran 90 module.

    Attributes:
        parent_file_path: The path to the Fortran 90 file the module
          is in.
        contents: The lines of code that make up the module.
        block_name: The name given to the module.
        variables: A list of all the variables in the module.
        subprograms: A list of CodeBlock objects contained by the code
          block being instantiated.
    """

    def __init__(self, parent_file_path: str, contents: List[CodeStatement], subprograms: List[CodeBlock]) -> None:
        """Initialises a module object."""

        super().__init__(parent_file_path, contents)
        self.block_name = self._find_block_name("MODULE")
        self.variables = self._find_variable_declarations()
        self.subprograms = subprograms
