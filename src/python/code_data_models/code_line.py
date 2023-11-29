from typing import List

from .code_pattern import CodePattern


class CodeLine:
    def __init__(self, line_content: str) -> None:
        self.line_content: str = line_content
        self.matched_patterns: List[CodePattern] = []

    def add_pattern(self, pattern_type: CodePattern) -> None:
        self.matched_patterns.append(pattern_type)

    def has_matched_patterns(self) -> bool:
        return len(self.matched_patterns) > 0

    def contains_end_statement(self) -> bool:
        return any(CodePattern.END in pattern for pattern in self.matched_patterns)  # type: ignore[operator]

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}({self.line_content!r}, {self.matched_patterns})"
