import re
from typing import Iterable, List

from code_data_models.code_block import CodeBlock
from code_data_models.code_pattern import CodePattern, CodePatternRegex
from code_data_models.code_statement import CodeStatement
from code_data_models.fortran_do_loop import FortranDoLoop
from code_data_models.fortran_function import FortranFunction
from code_data_models.fortran_if_block import FortranIfBlock
from code_data_models.fortran_interface import FortranInterface
from code_data_models.fortran_module import FortranModule
from code_data_models.fortran_program import FortranProgram
from code_data_models.fortran_subroutine import FortranSubroutine
from code_data_models.fortran_type import FortranType
from parsers.code_parser_stack import CodeParserStack
from utils.comment_finder import find_comment
from utils.repr_builder import build_repr_from_attributes

from .digital_file import DigitalFile

CODE_BLOCKS_THAT_SUPPORT_SUBPROGRAMS = [
    FortranFunction,
    FortranDoLoop,
    FortranIfBlock,
    FortranModule,
    FortranProgram,
    FortranSubroutine,
]


class FortranFile(DigitalFile):
    """A file with the .f90 extension. Stores Fortran 90 code.

    Attributes:
        path_from_root: The path to the file, starting from the root of
          the codebase.
        contents: A list of all the lines of code in the file.
        components: The detected code blocks that make up the file.
    """

    def __init__(self, path_from_root: str, contents: Iterable[str] = []) -> None:
        """Initialises a Fortran file object.

        Args:
            path_from_root: The path to the file, starting from the root
              of the codebase.
            contents: The lines of code that make up the file.
        """

        super().__init__(path_from_root)

        self.contents: List[CodeStatement] = []
        for index, line in enumerate(contents):
            # This stops several commands on one line being counted as a
            # single statement.
            all_statements = self._split_statements(line)

            for statement in all_statements:
                # Line numbers in almost all editors start at 1, hence
                # the increment of index here.
                self.contents.append(CodeStatement((index + 1), statement))

        self.components: List[CodeBlock] = self._parse_code_blocks()

    def get_snippet(self, start_line: int, end_line: int) -> List[CodeStatement]:
        """Returns a slice of the file's contents.

        Returns all statements in the file with line numbers between the
        given start and end values (inclusive). The returned list may
        end up being slightly longer than (end - start) items, since it
        is legal in Fortran to put multiple statements on the same line
        by using semicolons.

        Args:
            start_line: The number of the first line to include in the
              slice.
            end_line: The final line number to include in the slice.

        Returns:
            A list of all CodeLine objects found with line numbers in
            the given range (inclusive).

        Raises:
            ValueError: The provided start or end line number is below
              1.
        """

        if start_line < 1 or end_line < 1:
            raise ValueError("Line numbers cannot be less than 1.")

        statements_in_range = []
        for statement in self.contents:
            if start_line <= statement.line_number <= end_line:
                statements_in_range.append(statement)

        return statements_in_range

    def _parse_code_blocks(self) -> List[CodeBlock]:
        """Analyses the file's contents and creates code block objects.

        Analyses the file's contents, working out where the different
        code blocks contained in the file start and end according to
        the regex patterns they match. The contents are then separated
        into their respective blocks and added to a list of 'components'
        that make up the file.

        Returns:
            A list of code blocks that make up the Fortran file.
        """

        code_patterns = [
            (CodePattern.DO_LOOP, CodePatternRegex.DO_LOOP),
            (CodePattern.DO_LOOP_END, CodePatternRegex.DO_LOOP_END),
            (CodePattern.FUNCTION, CodePatternRegex.FUNCTION),
            (CodePattern.FUNCTION_END, CodePatternRegex.FUNCTION_END),
            (CodePattern.IF_BLOCK, CodePatternRegex.IF_BLOCK),
            (CodePattern.IF_BLOCK_END, CodePatternRegex.IF_BLOCK_END),
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

        stack = CodeParserStack()
        all_code_block_types = {
            CodePattern.DO_LOOP: FortranDoLoop,
            CodePattern.FUNCTION: FortranFunction,
            CodePattern.IF_BLOCK: FortranIfBlock,
            CodePattern.INTERFACE: FortranInterface,
            CodePattern.MODULE: FortranModule,
            CodePattern.PROGRAM: FortranProgram,
            CodePattern.SUBROUTINE: FortranSubroutine,
            CodePattern.TYPE: FortranType,
        }

        found_components = []

        for line in self.contents:
            if not line.has_matched_patterns():
                continue

            if not line.is_end_statement() and line.has_matched_patterns():
                stack.push(line.matched_patterns[0], line.line_number)

            if line.is_end_statement():
                block_type, start_line, subprograms = stack.pop()
                block_contents = self.get_snippet(start_line, line.line_number)
                new_block_type = all_code_block_types[block_type]
                if new_block_type in CODE_BLOCKS_THAT_SUPPORT_SUBPROGRAMS:
                    block_object = new_block_type(self.path_from_root, block_contents, subprograms)
                else:
                    # Something has went wrong in our parsing logic if
                    # the stack item we popped is for a type of code
                    # block that doesn't support subprograms, but we
                    # somehow ended up with subprograms anyway...
                    assert subprograms == []
                    block_object = new_block_type(self.path_from_root, block_contents)

                if stack.peek() is not None:
                    stack.add_subprogram_to_top_item(block_object)
                else:
                    found_components.append(block_object)

        assert stack.is_empty
        return found_components  # A non-empty stack means a code block has not been resolved somewhere

    def _split_statements(self, line: str) -> List[str]:
        """Splits statements separated by semicolons into a list."""

        # We will remove comments, split the line using ";", and then
        # add the comment back. This is to avoid any comments getting
        # unnecessarily split.
        comment = find_comment(line)
        if comment:
            line = line.replace(comment, "")

        statement_list = line.split(";")
        statement_list[-1] += comment or ""

        return [line.strip() for line in statement_list]

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            target_object=self,
            file_name=self.file_name,
            lines_of_code=len(self),
            code_blocks=len(self.components),
        )

    def __len__(self) -> int:
        if not self.contents:
            return 0

        first_statement = self.contents[0]
        last_statement = self.contents[-1]

        # Add 1 to final result to account for line numbers starting at
        # 1 e.g. A 5 line long file will do 5 - 1 and end up with length
        # 4... so add 1.
        return (last_statement.line_number - first_statement.line_number) + 1
