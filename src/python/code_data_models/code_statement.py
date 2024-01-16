from typing import List

from utils.repr_builder import build_repr_from_attributes

from .code_pattern import CodePattern


class CodeStatement:
    """A single Fortran instruction.

    Attributes:
        line_number: The line number of the code statement in its parent file.
          Statements on the same line separated by semicolons will have the
          same line number.
        content: The string contents of the statement.
        matched_patterns: A list of CodePatterns that the statement could possibly be.
    """

    def __init__(self, line_number: int, content: str) -> None:
        """Initialises a code statement object.

        Args:
            line_number: The line number of the code statement in its
              parent file.
            content: The string contents of the statement.
        """

        self.line_number: int = line_number
        self.content: str = content
        self.matched_patterns: List[CodePattern] = []

    def add_pattern(self, pattern_type: CodePattern) -> None:
        """Adds a code pattern into the list of matched patterns for the statement.

        Args:
            pattern_type: The code pattern that the statement matches.
        """

        self.matched_patterns.append(pattern_type)

    def has_matched_patterns(self) -> bool:
        """Checks if the statement has matched any Fortran code patterns.

        Returns:
            A boolean that is True when there is at least one pattern matched for
            the statement, otherwise False.
        """

        return len(self.matched_patterns) > 0

    def is_end_statement(self) -> bool:
        """Checks if the statement has matched any Fortran END statements.

        Returns:
            A boolean that is True when there is at least one END pattern matched for
            the statement, otherwise False.
        """

        return any(CodePattern.END in pattern for pattern in self.matched_patterns)  # type: ignore[operator]

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            class_name=type(self).__name__,
            line_number=self.line_number,
            content=self.content,
        )