from typing import Generator

from . import DigitalFile


class FortranFile(DigitalFile):
    def __init__(self, file_name: str, contents: Generator[str, None, None]) -> None:
        super().__init__(file_name)
        self.contents: Generator[str, None, None] = contents
