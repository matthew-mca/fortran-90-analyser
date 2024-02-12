import re
from abc import ABC, abstractmethod
from typing import List, Self, Tuple

from utils.comment_finder import remove_comment_from_line
from utils.repr_builder import build_repr_from_attributes

from .code_pattern import CodePatternRegex
from .code_statement import CodeStatement
from .variable import Variable


class CodeBlock(ABC):
    """A logical grouping of lines of Fortran 90 code.

    This class is used as an abstract base for all the different types of blocks in Fortran 90.
    That way, we can include any attributes/behaviours that apply to every single type of Fortran 90
    code block in this class. Any and all code blocks that become supported in the application should
    inherit from this class.

    Attributes:
        parent_file_path: The path to the Fortran 90 file the code block
          is in.
        contents: The lines of code that make up the block.
    """

    @abstractmethod
    def __init__(self, parent_file_path: str, contents: List[CodeStatement]) -> None:
        """Initialises a code block containing the provided lines of code.

        Args:
            parent_file_path: The path to the Fortran 90 file the code block is in.
            contents: The lines of code that make up the block.
        """

        self.parent_file_path = parent_file_path
        self.contents = contents

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            target_object=self,
            lines_of_code=len(self),
        )

    def __len__(self) -> int:
        if not self.contents:
            return 0

        # Add 1 to final result to account for line numbers starting at 1
        # e.g. A 5 line long file will do 5 - 1 and end up with length 4... so add 1.
        return (self.end_line_number - self.start_line_number) + 1

    @property
    def start_line_number(self) -> int:
        """The line number of the first line in the code block."""

        return self.contents[0].line_number

    @property
    def end_line_number(self) -> int:
        """The line number of the last line in the code block."""

        return self.contents[-1].line_number

    def contains_block(self, other: Self) -> bool:
        """Checks if the code block contains another provided block.

        Checks if the code block object the function is called on
        contains another provided code block. A code block contains
        another block if the first block is part of the same file as the
        second, and if the first block starts BEFORE and ends AFTER the
        second block.

        Args:
            other: The code block that is checked to determine if it is
              contained within the first block.

        Returns:
            A boolean value that is True if the first code block
            contains the provided block, or False if it does not.
        """

        if self.parent_file_path != other.parent_file_path:
            return False

        return self.start_line_number < other.start_line_number and self.end_line_number > other.end_line_number

    def _find_block_name(self, block_type: str) -> str:
        """Parses the code block's name from its declaration.

        Args:
            block_type: The type of block calling the function. This
              value is used to find and remove the same word from the
              declaration string as part of the parsing behaviour.

        Returns:
            The name of the declared code block.
        """

        start_line = self.contents[0].content
        start_line = remove_comment_from_line(start_line)
        start_line = re.sub(rf"\b{block_type}\b", "", start_line, flags=re.IGNORECASE)

        return start_line.strip()

    def _find_variable_declarations(self) -> List[Variable]:
        """Parses the code block to find all the variables declared.

        Parses through all the lines of the code block and matches any
        lines that contain variable declarations. The declaration is
        then parsed to deduce what type of variables are being declared,
        any additional attributes given as part of the declaration, the
        amount of variables being declared, and any initial values
        assigned to the variable(s). These variables are also checked
        against the rest of the block to see if there is a chance they
        are unused in the remainder of the block.

        Returns:
            A list of variable objects that were found within the code
            block.
        """

        found_variables = []

        for content_index in range(len(self.contents)):
            line_content = self.contents[content_index].content
            if not re.match(CodePatternRegex.VARIABLE_DECLARATION, line_content, re.IGNORECASE):
                continue

            line_content = remove_comment_from_line(line_content)

            declaration_parts = line_content.split("::")
            # Variables can have various attributes that follow the
            # data type, but these aren't required
            data_type, attributes = self._parse_variable_type_and_attributes(declaration_parts[0])

            variable_list = declaration_parts[1].split(",")
            for variable in variable_list:
                # Split on the "=" sign in case a value is assigned
                # to the variable on the same line
                variable_parts = variable.split("=")
                variable_name = variable_parts[0].strip()
                # This next bit was added after seeing that arrays with their length declared as
                # part of the variable name, ended up storing the name with the length part still
                # on the end of it... so now we search for it and remove.
                if re.search(r"\(\d+\)", variable_name) is not None:
                    bracket_index = variable_name.index("(")
                    variable_name = variable_name[:bracket_index]

                # Check the remaining lines to determine if
                # there is a possibility the variable is unused
                possibly_unused = True
                for line in self.contents[content_index + 1 :]:  # noqa: E203
                    if re.search(rf"\b{variable_name}\b", line.content):
                        possibly_unused = False

                found_variables.append(
                    Variable(
                        data_type=data_type,
                        attributes=attributes,
                        name=variable_name,
                        parent_file_path=self.parent_file_path,
                        line_declared=self.contents[content_index].line_number,
                        possibly_unused=possibly_unused,
                    )
                )

        return found_variables

    def _parse_variable_type_and_attributes(self, type_and_attr_string: str) -> Tuple[str, List[str]]:
        """Parses the first half of a variable declaration.

        Parses the parts of a Fortran variable declaration before the
        '::' part to figure out what data type and attributes are
        included as part of the variable declaration.

        Args:
            type_and_attr_string: The first part of a Fortran variable
              declaration (before the '::').

        Returns:
            A tuple (data_type, attributes) where 'data_type' is the
            Fortran data type detected for the declaration, and
            'attributes' is a list of the variable attributes included
            after the data type.
        """

        # This function draws some inspiration from the comment finder
        # util, in that we need to parse the data type and attributes of
        # a variable to find commas that are NOT inside of an attribute,
        # e.g. inside the DIMENSION attribute. We can then split on the
        # commas found.
        if "," not in type_and_attr_string:
            return type_and_attr_string.strip().upper(), []

        type_and_attr_parts = []
        open_bracket_count = 0
        start_of_slice = 0

        for i in range(len(type_and_attr_string)):
            if (current_char := type_and_attr_string[i]) not in (",", "(", ")"):
                continue
            elif current_char == "(":
                open_bracket_count += 1
            elif current_char == ")":
                open_bracket_count -= 1
            elif open_bracket_count == 0:
                type_and_attr_parts.append(type_and_attr_string[start_of_slice:i].strip().upper())
                # index i is on a comma at this point, and we're not that
                # interested in keeping it so add 1 to the new slice starting point
                start_of_slice = i + 1

        # Add the final split piece
        type_and_attr_parts.append(type_and_attr_string[start_of_slice:].strip().upper())

        return type_and_attr_parts[0], type_and_attr_parts[1:]
