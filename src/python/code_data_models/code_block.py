from abc import ABC, abstractmethod
from typing import List

from utils.repr_builder import build_repr_from_attributes

from .code_line import CodeLine


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
    def __init__(self, contents: List[CodeLine]) -> None:
        """Initialises a code block containing the provided lines of code.

        Args:
            contents: The lines of code that will make up the block.
        """

        self.contents = contents

    # TODO: See if removing abstractmethod here can reduce unnecessary
    # calls to super in child classes while working on issue 14
    @abstractmethod
    def get_snippet(self, start_index: int, end_index: int) -> List[CodeLine]:
        """Returns a slice of the block's contents.

        Args:
            start_index: The index of the first line to include in the slice.
            end_index: The index of where to end the slice. The line at this
              index is not included.
        """

        return self.contents[start_index:end_index]

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            class_name=type(self).__name__,
            lines_of_code=len(self.contents),
        )
