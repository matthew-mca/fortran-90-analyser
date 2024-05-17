import os

from utils.repr_builder import build_repr_from_attributes


class DigitalFile:
    """A digital computer file.

    Attributes:
        path_from_root: The path to the file, starting from the root of
          the codebase.
        file_name: The name of the file itself.
        failed_fortran_parse: This value is true when an object was
          supposed to be a child instance of this class (FortranFile),
          but parsing failed and so it fell back to being a DigitalFile
          instance.
    """

    def __init__(self, path_from_root: str, failed_fortran_parse: bool = False) -> None:
        """Initialises a file object.

        Args:
            path_from_root: The path to the file, starting from the root
              of the codebase.
            failed_fortran_parse: This value is true when an object was
              supposed to be a child instance of this class (FortranFile),
              but parsing failed and so it fell back to being a DigitalFile
              instance.
        """

        self.path_from_root: str = path_from_root
        self.file_name = os.path.split(self.path_from_root)[1]
        self.failed_fortran_parse = failed_fortran_parse

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            target_object=self,
            file_name=self.file_name,
        )
