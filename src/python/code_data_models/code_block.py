from abc import ABC, abstractmethod
from typing import List

from .code_line import CodeLine


class CodeBlock(ABC):
    @abstractmethod
    def __init__(self, contents: List[CodeLine]) -> None:
        self.contents = contents

    @abstractmethod
    def get_snippet(self, start_index: int, end_index: int) -> List[CodeLine]:
        return self.contents[start_index:end_index]
