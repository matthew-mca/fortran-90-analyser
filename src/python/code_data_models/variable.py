from types import NotImplementedType
from typing import Any, List, Union

from utils.repr_builder import build_repr_from_attributes


class Variable:
    """A representation of a variable in Fortran 90.

    Attributes:
        ALL_DATA_TYPES: A list of all the possible built-in data types
          that a variable can have in Fortran 90.
        data_type: The declared data type for the variable.
        attributes: A list of all the attributes declared as part of the
          variable.
        name: The name given to the variable.
        parent_file_path: The path to the Fortran 90 file the variable
          is in.
        line_declared: The number of the line on which the variable is
          declared.
        possibly_unused: A bool indicating whether or not there is a
          possibility the variable is not used after declaration.
    """

    ALL_DATA_TYPES = [
        "CHARACTER",
        "COMPLEX",
        "DOUBLE COMPLEX",
        "DOUBLE PRECISION",
        "INTEGER",
        "LOGICAL",
        "REAL",
    ]

    def __init__(
        self,
        data_type: str,
        attributes: List[str],
        name: str,
        parent_file_path: str,
        line_declared: int,
        possibly_unused: bool,
    ):
        """Initialises a Variable object."""

        self.data_type = data_type
        self.attributes = attributes
        self.name = name
        self.parent_file_path = parent_file_path
        self.line_declared = line_declared
        self.possibly_unused = possibly_unused

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            target_object=self,
            data_type=self.data_type,
            name=self.name,
            parent_file_path=self.parent_file_path,
        )

    def __eq__(self, other: Any) -> Union[bool, NotImplementedType]:
        if not isinstance(other, Variable):
            return NotImplemented

        # We compare every attribute of the two variables, EXCEPT for the
        # possibly_unused field. This is because larger program units may contain
        # multiple subprograms that use the same local variable names, and therefore
        # there is a small chance that larger program units may incorrectly mark an
        # unused variable as used, resulting in the same variable having two different
        # possibly_unused values depending on its parent code block.
        self_dict = {k: v for k, v in self.__dict__.items() if k != "possibly_unused"}
        other_dict = {k: v for k, v in other.__dict__.items() if k != "possibly_unused"}

        return self_dict == other_dict

    @property
    def is_pointer(self) -> bool:
        """A bool that states if the variable is a pointer or not."""

        return "POINTER" in self.attributes

    @property
    def is_array(self) -> bool:
        """A bool that states if the variable is an array or not."""

        # We can't just check DIMENSION is in the attribute list due to the
        # varying bracket part of the DIMENSION attribute, e.g. DIMENSION(13, 9)
        return any("DIMENSION" in attribute for attribute in self.attributes)
