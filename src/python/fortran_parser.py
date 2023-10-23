from typing import Generator


def parse_file(file_path: str) -> Generator[str, None, None]:
    with open(file_path, "r") as f:
        line = f.readline()
        while line:
            yield line
            line = f.readline()
