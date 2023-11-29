from typing import List, Tuple

from dataclasses import dataclass


@dataclass
class CodeParserStackItem:
    item_type: str
    index: int


class CodeParserStack:
    def __init__(self) -> None:
        self.items: List[CodeParserStackItem] = []

    def push(self, statement_type: str, index: int) -> None:
        self.items.append(CodeParserStackItem(statement_type, index))

    def pop(self) -> Tuple[str, int]:
        stack_item = self.items.pop()
        return stack_item.item_type, stack_item.index

    def peek(self) -> Tuple[str, int]:
        stack_item = self.items[-1]
        return stack_item.item_type, stack_item.index

    def size(self) -> int:
        return len(self.items)

    def is_empty(self) -> bool:
        return self.size() == 0
