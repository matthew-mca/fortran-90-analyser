import pytest

from code_data_models.code_pattern import CodePattern
from code_data_models.fortran_function import FortranFunction
from parsers.code_parser_stack import CodeParserStack, CodeParserStackItem, EmptyStackError
from tests.object_factory import random_fortran_function


class TestCodeParserStack:
    @pytest.fixture
    def empty_stack(self):
        return CodeParserStack()

    def test_push_and_pop(self, empty_stack):
        assert empty_stack.size == 0

        empty_stack.push(CodePattern.PROGRAM, 17)
        empty_stack.push(CodePattern.MODULE, 24)
        assert empty_stack.size == 2
        assert all(isinstance(stack_item, CodeParserStackItem) for stack_item in empty_stack.items)

        item_1, item_2, item_3 = empty_stack.pop()
        assert item_1 == CodePattern.MODULE
        assert item_2 == 24
        assert item_3 == []

        assert empty_stack.size == 1

    def test_peek(self, empty_stack):
        assert empty_stack.size == 0

        empty_stack.push(CodePattern.PROGRAM, 5)
        assert empty_stack.size == 1

        item_1, item_2, item_3 = empty_stack.peek()
        assert item_1 == CodePattern.PROGRAM
        assert item_2 == 5
        assert item_3 == []

        assert empty_stack.size == 1

    def test_is_empty(self, empty_stack):
        assert empty_stack.is_empty

        empty_stack.push(CodePattern.TYPE, 73)
        assert not empty_stack.is_empty

        empty_stack.peek()
        assert not empty_stack.is_empty

        empty_stack.pop()
        assert empty_stack.is_empty

    def test_code_parser_stack_repr(self, empty_stack):
        expected_repr = "CodeParserStack(item_count=0)"
        assert repr(empty_stack) == expected_repr

    def test_pop_empty_stack(self, empty_stack):
        with pytest.raises(EmptyStackError):
            empty_stack.pop()

    def test_peek_empty_stack(self, empty_stack):
        assert empty_stack.peek() is None

    def test_add_subprogram_to_top_item(self, empty_stack):
        empty_stack.push(CodePattern.PROGRAM, 1)
        empty_stack.push(CodePattern.MODULE, 2)

        empty_stack.add_subprogram_to_top_item(random_fortran_function())

        module_info = empty_stack.pop()
        program_info = empty_stack.pop()

        program_subprograms = program_info[2]
        module_subprograms = module_info[2]

        assert program_subprograms == []

        assert len(module_subprograms) == 1
        assert isinstance(module_subprograms[0], FortranFunction)
