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

    This class is used as an abstract base for all the different types
    of blocks in Fortran 90. That way, we can include any
    attributes/behaviours that apply to every single type of Fortran 90
    code block in this class. Any and all code blocks that become
    supported in the application should inherit from this class.

    Attributes:
        parent_file_path: The path to the Fortran 90 file the code block
          is in.
        contents: The lines of code that make up the block.
        start_line_number: The line number of the first line in the
          block.
        end_line_number: The line number of the final line in the block.
    """

    @abstractmethod
    def __init__(self, parent_file_path: str, contents: List[CodeStatement]) -> None:
        """Initialises a code block.

        Args:
            parent_file_path: The path to the Fortran 90 file the code
              block is in.
            contents: The lines of code that make up the block.
        """

        self.parent_file_path = parent_file_path
        self.contents = contents
        self.start_line_number = self.contents[0].line_number
        self.end_line_number = self.contents[-1].line_number

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            target_object=self,
            lines_of_code=len(self),
        )

    def __len__(self) -> int:
        # Add 1 to final result to account for line numbers starting at
        # 1 e.g. A 5 line long file will do 5 - 1 and end up with length
        # 4... so add 1.
        return (self.end_line_number - self.start_line_number) + 1

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

    def get_variables_not_in_subprograms(self) -> List[Variable]:
        """Returns all the variables not present in any subprograms.

        Collects all of the variables stored in each subprogram inside
        the code block. Once all these variables have been collected,
        the function creates and returns a list containing ONLY the
        variables not found in this list of subprogram variables. This
        means that only the variables at the block's widest scope are
        returned.

        Returns:
            The list of variables stored for the code block, minus any
            variables that can also be found in the block's subprograms.

        Raises:
            TypeError: The object calling this function does not support
              subprograms and/or variables. Certain child classes of
              CodeBlock do not have these attributes.
        """

        if not hasattr(self, "subprograms") or not hasattr(self, "variables"):
            raise TypeError("Current code block type does not support subprograms and/or variables.")

        all_subprogram_variables: List[Variable] = []
        for subprogram in self.subprograms:
            all_subprogram_variables.extend(getattr(subprogram, "variables", []))

        return [var for var in self.variables if var not in all_subprogram_variables]

    def get_all_subprograms(self) -> List[Self]:
        """Gets a list of all subprograms inside of the code block.

        This function gets all of the subprograms that can be found for
        the code block, regardless of how deeply nested it is. Any and
        all subprograms are included in the final list without any
        nesting.

        Returns:
            A list of all the subprograms found within the code block.

        Raises:
            TypeError: The object calling this function does not support
              subprograms. Certain child classes of CodeBlock do not
              have this attribute.
        """

        if not hasattr(self, "subprograms"):
            raise TypeError("Current code block type does not support subprograms.")

        lower_level_programs = []
        for program in getattr(self, "subprograms", []):
            try:
                lower_level_programs += program.get_all_subprograms()
            except TypeError:
                continue

        return self.subprograms + lower_level_programs

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

            declaration_parts = self._split_outside_quotes(line_content, "::")
            # Variables can have various attributes that follow the
            # data type, but these aren't required
            data_type, attributes = self._parse_variable_type_and_attributes(declaration_parts[0])

            variable_list = self._split_outside_quotes(declaration_parts[1], ",")
            for variable in variable_list:
                is_array = any("DIMENSION" in attribute for attribute in attributes)
                # Split on the "=" sign in case a value is assigned
                # to the variable on the same line
                variable_parts = self._split_outside_quotes(variable, "=")
                variable_name = variable_parts[0].strip()
                # This next bit was added after seeing that arrays with
                # their length declared as part of the variable name,
                # ended up storing the name with the length part still
                # on the end of it... so now we search for it and
                # remove.
                if re.search(r"\(\d+\)", variable_name) is not None:
                    # TODO: Add testing for this case when adding
                    # integration testing
                    is_array = True
                    bracket_index = variable_name.index("(")
                    variable_name = variable_name[:bracket_index]

                # Check the remaining lines to determine if
                # there is a possibility the variable is unused
                possibly_unused = True
                for line in self.contents[content_index + 1 :]:
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
                        is_array=is_array,
                    )
                )

        return found_variables

    def _parse_variable_type_and_attributes(self, type_and_attr_string: str) -> Tuple[str, List[str]]:
        """Parses the first half of a variable declaration.

        Parses the elements of a Fortran variable declaration before the
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
                # index i is on a comma at this point, and we're not
                # that interested in keeping it so add 1 to the new
                # slice starting point
                start_of_slice = i + 1

        # Add the final split piece
        type_and_attr_parts.append(type_and_attr_string[start_of_slice:].strip().upper())

        return type_and_attr_parts[0], type_and_attr_parts[1:]

    def _split_outside_quotes(self, string_to_split: str, delimiter: str) -> List[str]:
        split_parts = []

        # Set and unset as we enter and exit quotes
        active_quote_char = None
        quote_chars = ("'", '"')
        start_of_slice = 0

        for i in range(len(string_to_split)):
            current_str = string_to_split[start_of_slice:i]
            reverse = current_str[::-1]

            if delimiter == reverse[: len(delimiter)] and active_quote_char is None:
                # Reaching here means we found our delimiter outside
                # quotes
                split_parts.append(string_to_split[start_of_slice : (i - len(delimiter))])
                start_of_slice = i

            if string_to_split[i] in quote_chars and active_quote_char is None:
                active_quote_char = string_to_split[i]
            elif active_quote_char is not None:
                if string_to_split[i] == active_quote_char:
                    active_quote_char = None

        # Due to the fact that in our loop we check if we need to split,
        # THEN we check if we have left a quoted string, if the supplied
        # string argument ends with a quote character, we have to do one
        # final check outside the loop to see if a split is needed.
        if string_to_split[start_of_slice:][-1] in quote_chars:
            split_parts.append(string_to_split[start_of_slice:])
        else:
            split_parts.extend(string_to_split[start_of_slice:].split(delimiter))

        return split_parts
