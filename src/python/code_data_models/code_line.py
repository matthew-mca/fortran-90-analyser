from typing import List

from .code_pattern import CodePattern


class CodeLine:
    """A single line of code.

    Attributes:
        line_content: The string contents of the line.
        matched_patterns: A list of CodePatterns that the line could possibly be.
    """

    def __init__(self, line_content: str) -> None:
        """Initialises a code line object.

        Args:
            line_content: The string contents of the line.
        """

        self.line_content: str = line_content
        self.matched_patterns: List[CodePattern] = []

    def add_pattern(self, pattern_type: CodePattern) -> None:
        """Adds a code pattern into the list of matched patterns for the line.

        Args:
            pattern_type: The code pattern that the line matches.
        """

        self.matched_patterns.append(pattern_type)

    def has_matched_patterns(self) -> bool:
        """Checks if the line has matched any Fortran code patterns.

        Returns:
            A boolean that is True when there is at least one pattern matched for
            the line, otherwise False.
        """

        return len(self.matched_patterns) > 0

    def contains_end_statement(self) -> bool:
        """Checks if the line has matched any Fortran END statements.

        Returns:
            A boolean that is True when there is at least one END pattern matched for
            the line, otherwise False.
        """

        return any(CodePattern.END in pattern for pattern in self.matched_patterns)  # type: ignore[operator]

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}({self.line_content!r}, {self.matched_patterns})"
