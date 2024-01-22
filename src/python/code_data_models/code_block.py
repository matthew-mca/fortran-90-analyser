from abc import ABC, abstractmethod
from typing import List

from utils.repr_builder import build_repr_from_attributes

from .code_statement import CodeStatement


class CodeBlock(ABC):
    """A logical grouping of lines of Fortran 90 code.

    This class is used as an abstract base for all the different types of blocks in Fortran 90.
    That way, we can include any attributes/behaviours that apply to every single type of Fortran 90
    code block in this class. Any and all code blocks that become supported in the application should
    inherit from this class.

    Attributes:
        contents: The lines of code that make up the block.
    """

    @abstractmethod
    def __init__(self, contents: List[CodeStatement]) -> None:
        """Initialises a code block containing the provided lines of code.

        Args:
            contents: The lines of code that will make up the block.
        """

        self.contents = contents

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            class_name=type(self).__name__,
            lines_of_code=len(self),
        )

    def __len__(self) -> int:
        if not self.contents:
            return 0

        first_statement = self.contents[0]
        last_statement = self.contents[-1]

        # Add 1 to final result to account for line numbers starting at 1
        # e.g. A 5 line long file will do 5 - 1 and end up with length 4... so add 1.
        return (last_statement.line_number - first_statement.line_number) + 1
