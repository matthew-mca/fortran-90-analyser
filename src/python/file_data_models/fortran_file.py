import re
from typing import Iterable, List, Optional

from code_data_models.code_block import CodeBlock
from code_data_models.code_line import CodeLine
from code_data_models.code_pattern import CodePattern, CodePatternRegex
from parsers.code_parser import CodeParser
from parsers.code_parser_stack import CodeParserStack

from .digital_file import DigitalFile


class FortranFile(DigitalFile):
    def __init__(self, file_name: str, contents: Iterable[str] = []) -> None:
        super().__init__(file_name)
        self.contents: List[CodeLine] = [CodeLine(line) for line in contents]
        self.components: List[CodeBlock] = []
        self._tag_lines()
        self._parse_code_blocks()

    def get_snippet(self, start_index: int, end_index: int) -> List[CodeLine]:
        return self.contents[start_index:end_index]

    def _tag_lines(self) -> None:
        code_patterns = [
            (CodePattern.MODULE, CodePatternRegex.MODULE),
            (CodePattern.MODULE_END, CodePatternRegex.MODULE_END),
            (CodePattern.PROGRAM, CodePatternRegex.PROGRAM),
            (CodePattern.PROGRAM_END, CodePatternRegex.PROGRAM_END),
            (CodePattern.TYPE, CodePatternRegex.TYPE),
            (CodePattern.TYPE_END, CodePatternRegex.TYPE_END),
        ]

        for line in self.contents:
            for pattern, pattern_regex in code_patterns:
                if re.match(pattern_regex, line.line_content):
                    line.add_pattern(pattern)

    def _parse_code_blocks(self) -> None:
        parser = CodeParser()
        stack = CodeParserStack()

        for index, line in enumerate(self.contents):
            if not line.has_matched_patterns():
                continue

            # TODO: This will definitely need changed to account for lines with semicolons,
            # but going to keep as is for the time being. When ready, add a test case for this.
            if not line.contains_end_statement() and line.has_matched_patterns():
                stack.push(line.matched_patterns[0], index)

            if line.contains_end_statement():
                block_type, start_index = stack.pop()
                block_contents = self.get_snippet(start_index, index) + [line]  # Include current line too
                self.components.append(parser.build_code_block_object(block_type, block_contents))

        assert stack.is_empty()  # A non-empty stack means a code block has not been resolved somewhere
