import pytest

from utils.comment_finder import find_comment


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
def test_find_comment(line, expected_result):
    assert find_comment(line) == expected_result
