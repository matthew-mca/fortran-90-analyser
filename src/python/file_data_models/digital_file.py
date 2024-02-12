import os

from utils.repr_builder import build_repr_from_attributes


class DigitalFile:
    """A digital computer file.

    Attributes:
        path_from_root: The path to the file, starting from the root of
          the codebase.
    """

    def __init__(self, path_from_root: str) -> None:
        """Initialises a file object.

        Args:
            path_from_root: The path to the file, starting from the root
              of the codebase.
        """

        self.path_from_root: str = path_from_root

    @property
    def file_name(self) -> str:
        """The name of the file."""

        return os.path.split(self.path_from_root)[1]

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            class_name=type(self).__name__,
            file_name=self.file_name,
        )
