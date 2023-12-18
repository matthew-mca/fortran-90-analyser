from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class CodeParserStackItem:
    """A stack item that holds info related to the start of a code block.

    Attributes:
        item_type: The type of code block start that was detected.
        index: The index at which the code block starts in the code being parsed.
    """

    item_type: str
    index: int


class CodeParserStack:
    """A stack that is used to keep track of where code blocks start and end.

    When the start of a certain type of code block is detected, the type of block
    and the index at which it starts are added into the stack in the form of a
    CodeParserStackItem. When an END statement is detected, the item at the top of
    the stack is popped off the stack. The info in the stack item can then be used
    along with the index of the corresponding END statement to construct a code block
    object.

    Attributes:
        items: A list of CodeParserStackItem instances.
    """

    def __init__(self) -> None:
        """Initialises an empty stack."""

        self.items: List[CodeParserStackItem] = []

    def push(self, statement_type: str, index: int) -> None:
        """Pushes a stack item onto the top of the stack.

        Args:
            statement_type: The type of program statement, e.g. the start of a program.
            index: The index of the statement in the code block it came from.
        """

        self.items.append(CodeParserStackItem(statement_type, index))

    def pop(self) -> Tuple[str, int]:
        """Pops the top stack item off of the stack and returns its values.

        Returns:
            A tuple (type, index), where 'type' is the type of program statement the
            line matched, and 'index' is the index of the line in the code it came from.
        """

        stack_item = self.items.pop()
        return stack_item.item_type, stack_item.index

    def peek(self) -> Tuple[str, int]:
        """Returns the values of the stack item at the top of the stack without removing it.

        Returns:
            A tuple (type, index), where 'type' is the type of program statement the
            line matched, and 'index' is the index of the line in the code it came from.
        """

        stack_item = self.items[-1]
        return stack_item.item_type, stack_item.index

    def size(self) -> int:
        """Returns the number of items currently in the stack."""

        return len(self.items)

    def is_empty(self) -> bool:
        """Checks if the stack is currently empty.

        Returns:
            A boolean value that is True when the stack is empty, otherwise False.
        """

        return self.size() == 0
