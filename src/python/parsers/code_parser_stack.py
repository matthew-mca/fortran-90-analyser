from dataclasses import dataclass
from typing import List, Optional, Tuple

from code_data_models.code_block import CodeBlock
from utils.repr_builder import build_repr_from_attributes


class EmptyStackError(Exception):
    pass


@dataclass
class CodeParserStackItem:
    """A stack item that holds info about the start of a code block.

    Attributes:
        item_type: The type of code block start that was detected.
        line_number: The line number at which the code block starts in
          the overall file.
        subprograms: A list of CodeBlock objects that have been found
          before the item has found its accompanying END statement.
    """

    item_type: str
    line_number: int
    subprograms: list

    def add_subprogram(self, subprogram: CodeBlock) -> None:
        """Adds a provided CodeBlock object to the stack item."""

        self.subprograms.append(subprogram)


class CodeParserStack:
    """A stack that keeps track of where code blocks start and end.

    When the start of a certain type of code block is detected, the type
    of block and the line number at which it starts are added into the
    stack in the form of a CodeParserStackItem. When an END statement is
    detected, the item at the top of the stack is popped off the stack.
    The info in the stack item can then be used along with the line
    number of the corresponding END statement to construct a code block
    object.

    Attributes:
        items: A list of CodeParserStackItem instances.
    """

    def __init__(self) -> None:
        """Initialises an empty stack."""

        self.items: List[CodeParserStackItem] = []

    def push(self, statement_type: str, line_number: int) -> None:
        """Pushes a stack item onto the top of the stack.

        Args:
            statement_type: The type of program statement, e.g. the
              start of a program.
            line_number: The line number of the statement in the file it
              came from.
        """

        self.items.append(CodeParserStackItem(statement_type, line_number, []))

    def pop(self) -> Tuple[str, int, List[CodeBlock]]:
        """Removes the top item off of the stack and returns its values.

        Returns:
            A tuple (type, line_number, subprograms), where 'type' is
            the type of program statement the line matched,
            'line_number' is the number of the line in the file it came
            from, and 'subprograms' is a list of CodeBlock objects that
            have been found before the item has found its accompanying
            END statement.

        Raises:
            EmptyStackError: A pop was attempted while the stack was
              empty.
        """

        if self.is_empty:
            raise EmptyStackError("Cannot pop: stack is empty")

        stack_item = self.items.pop()
        return stack_item.item_type, stack_item.line_number, stack_item.subprograms

    def peek(self) -> Optional[Tuple[str, int, List[CodeBlock]]]:
        """Previews the values of the item at the top of the stack.

        Returns the values of the item at the top of the stack, but
        does not remove the item from the top of the stack.

        Returns:
            A tuple (type, line_number, subprograms), where 'type' is
            the type of program statement the line matched,
            'line_number' is the number of the line in the file it came
            from, and 'subprograms' is a list of CodeBlock items that
            have been found before the item has found its accompanying
            END statement. If the stack is empty, 'None' is returned.
        """

        if self.is_empty:
            return None

        stack_item = self.items[-1]
        return stack_item.item_type, stack_item.line_number, stack_item.subprograms

    def add_subprogram_to_top_item(self, subprogram: CodeBlock) -> None:
        """Adds a CodeBlock to the item at the top of the stack."""

        top_item = self.items[-1]
        top_item.add_subprogram(subprogram)

    @property
    def size(self) -> int:
        """The number of items currently in the stack."""

        return len(self.items)

    @property
    def is_empty(self) -> bool:
        """Indicates if the stack is currently empty or not.

        Returns:
            A boolean value that is True when the stack is empty,
            otherwise False.
        """

        return self.size == 0

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            target_object=self,
            item_count=self.size,
        )
