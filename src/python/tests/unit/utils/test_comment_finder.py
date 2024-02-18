import pytest

from utils.comment_finder import find_comment, remove_comment_from_line


class TestCommentFinder:
    @pytest.mark.parametrize(
        "line,expected_result",
        [
            ("test command", None),
            ("test command ! comment", "! comment"),
            ("!", "!"),
            ("!  ! ! Test comment", "!  ! ! Test comment"),
            ("Print *, 'Hello World!'", None),
            ('Print *, "Hello World!"', None),
            ("Print *, 'Hello World!' ! comment", "! comment"),
        ],
    )
    def test_find_comment(self, line, expected_result):
        assert find_comment(line) == expected_result

    @pytest.mark.parametrize(
        "line,expected_result",
        [
            ("test command", "test command"),
            ("test command ! comment", "test command "),
            ("!", ""),
            ("!  ! ! Test comment", ""),
            ("Print *, 'Hello World!'", "Print *, 'Hello World!'"),
            ('Print *, "Hello World!"', 'Print *, "Hello World!"'),
            ("Print *, 'Hello World!' ! comment", "Print *, 'Hello World!' "),
        ],
    )
    def test_remove_comment_from_line(self, line, expected_result):
        assert remove_comment_from_line(line) == expected_result
