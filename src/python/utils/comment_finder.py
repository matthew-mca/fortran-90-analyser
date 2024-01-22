from typing import Optional


def find_comment(line: str) -> Optional[str]:
    """Checks a line for the presence of a comment. Exclamation marks in quotes are ignored.

    Args:
        line: The line of code to be searched.

    Returns:
        The comment that was found in the line, or None if there is no comment.
    """

    if "!" not in line:
        return None

    # If we encounter an exclamation mark inside a quote, we know it's not a comment
    active_quote_char = None  # Set and unset as we enter and exit quotes
    quote_chars = ("'", '"')
    for i in range(len(line)):
        if line[i] not in ("!", "'", '"'):
            continue
        elif line[i] in quote_chars and active_quote_char is None:
            active_quote_char = line[i]
        elif active_quote_char is not None:
            if line[i] == active_quote_char:
                active_quote_char = None
        else:
            return line[i:]  # Reaching here means we found an exclamation mark outside quotes

    return None
