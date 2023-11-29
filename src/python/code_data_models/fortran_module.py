from typing import List

from .code_block import CodeBlock
from .code_line import CodeLine


class FortranModule(CodeBlock):
    def __init__(self, contents: List[CodeLine]) -> None:
        super().__init__(contents)

    def get_snippet(self, start_index: int, end_index: int) -> List[CodeLine]:
        return super().get_snippet(start_index, end_index)
