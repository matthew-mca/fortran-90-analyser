import re
from typing import Iterable, List

from code_data_models.code_block import CodeBlock
from code_data_models.code_pattern import CodePattern, CodePatternRegex
from code_data_models.code_statement import CodeStatement
from parsers.code_parser import CodeParser
from parsers.code_parser_stack import CodeParserStack
from utils.repr_builder import build_repr_from_attributes

from .digital_file import DigitalFile


class FortranFile(DigitalFile):
    """A file with the .f90 extension. Stores Fortran 90 code.

    Attributes:
        file_name: The name of the file.
        contents: A list of all the lines of code in the file.
        components: The detected code blocks that make up the file.
    """

    def __init__(self, file_name: str, contents: Iterable[str] = []) -> None:
        """Initialises a file object, and then tags and parses its contents.

        Args:
            file_name: The name of the file.
            contents: The lines of code that make up the file.
        """

        super().__init__(file_name)

        self.contents: List[CodeStatement] = []
        for index, line in enumerate(contents):
            # This stops several commands on one line being counted as a single statement
            all_statements = [statement.strip() for statement in line.split(";")]

            for statement in all_statements:
                # Line numbers in almost all editors start at 1, hence the increment of index here
                self.contents.append(CodeStatement((index + 1), statement))

        self.components: List[CodeBlock] = []
        self._tag_lines()
        self._parse_code_blocks()

    def get_snippet(self, start_line: int, end_line: int) -> List[CodeStatement]:
        """Returns a slice of the file's contents.

        Returns all statements in the file with line numbers between the given
        start and end values (inclusive). The returned list may end up being slightly
        longer than (end - start) items, since it is legal in Fortran to put multiple
        statements on the same line by using semicolons.

        Args:
            start_line: The number of the first line to include in the slice.
            end_line: The final line number to include in the slice.

        Returns:
            A list of all CodeLine objects found with line numbers in the given range
            (inclusive).

        Raises:
            ValueError: The provided start or end line number is below 1.
        """

        if start_line < 1 or end_line < 1:
            raise ValueError("Line numbers cannot be less than 1.")

        statements_in_range = []
        for statement in self.contents:
            if start_line <= statement.line_number <= end_line:
                statements_in_range.append(statement)

        return statements_in_range

    def _tag_lines(self) -> None:
        """Iterates through the file and tags each line with the possible patterns it could be."""

        code_patterns = [
            (CodePattern.FUNCTION, CodePatternRegex.FUNCTION),
            (CodePattern.FUNCTION_END, CodePatternRegex.FUNCTION_END),
            (CodePattern.INTERFACE, CodePatternRegex.INTERFACE),
            (CodePattern.INTERFACE_END, CodePatternRegex.INTERFACE_END),
            (CodePattern.MODULE, CodePatternRegex.MODULE),
            (CodePattern.MODULE_END, CodePatternRegex.MODULE_END),
            (CodePattern.PROGRAM, CodePatternRegex.PROGRAM),
            (CodePattern.PROGRAM_END, CodePatternRegex.PROGRAM_END),
            (CodePattern.SUBROUTINE, CodePatternRegex.SUBROUTINE),
            (CodePattern.SUBROUTINE_END, CodePatternRegex.SUBROUTINE_END),
            (CodePattern.TYPE, CodePatternRegex.TYPE),
            (CodePattern.TYPE_END, CodePatternRegex.TYPE_END),
        ]

        for line in self.contents:
            for pattern, pattern_regex in code_patterns:
                if re.match(pattern_regex, line.content, re.IGNORECASE):
                    line.add_pattern(pattern)

    def _parse_code_blocks(self) -> None:
        """Analyses the tagged lines in the file and creates code block objects."""

        parser = CodeParser()
        stack = CodeParserStack()

        for line in self.contents:
            if not line.has_matched_patterns():
                continue

            if not line.is_end_statement() and line.has_matched_patterns():
                stack.push(line.matched_patterns[0], line.line_number)

            if line.is_end_statement():
                block_type, start_line = stack.pop()
                block_contents = self.get_snippet(start_line, line.line_number)
                self.components.append(parser.build_code_block_object(block_type, block_contents))

        assert stack.is_empty()  # A non-empty stack means a code block has not been resolved somewhere

        # TODO: Should probably think about adding some sort of check that any END statements that
        # include the name of a function/program/module etc match up with the name in the declaration,
        # as it's not syntactically correct otherwise... not sure if in here or in the code parser though.
        # Edit: should probably add individual quirks for each code block as checks in their respective
        # child classes. Or in the respective functions in the parser...

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            class_name=type(self).__name__,
            file_name=self.file_name,
            lines_of_code=len(self.contents),
            code_blocks=len(self.components),
        )

    def __len__(self) -> int:
        if not self.contents:
            return 0

        first_statement = self.contents[0]
        last_statement = self.contents[-1]

        # Add 1 to final result to account for line numbers starting at 1
        # e.g. A 5 line long file will do 5 - 1 and end up with length 4... so add 1.
        return (last_statement.line_number - first_statement.line_number) + 1
