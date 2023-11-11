from typing import Iterable, Optional

from . import DigitalFile


class FortranFile(DigitalFile):
    def __init__(self, file_name: str, contents: Optional[Iterable] = None) -> None:
        super().__init__(file_name)
        self.contents: Optional[Iterable] = contents
