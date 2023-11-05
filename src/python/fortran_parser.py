import os
from typing import Dict, Generator, Union


class FortranParser:
    def parse_file(self, file_path: str) -> Generator[str, None, None]:
        with open(file_path, "r") as f:
            line = f.readline()
            while line:
                yield line
                line = f.readline()

    # TODO: Refactor to use Directory and File (and possibly File subclass for F90 files) classes
    def build_directory_tree(
        self,
        dir_path: str,
        include_non_fortran: bool = True,
    ) -> Dict[str, Union[Dict, Generator, None]]:
        """
        Builds out a representation of a specified directory.

        This function returns a represenation of the directory in the form of a dictionary on success,
        or raises a ValueError if the path supplied to the function is invalid.
        """
        dir_path = os.path.abspath(dir_path)  # Will resolve relative paths and leave absolute paths as is

        if not os.path.exists(dir_path):
            raise ValueError("Given path does not exist.")
        elif os.path.isfile(dir_path):
            raise ValueError("Specified path is a file, not a directory.")

        directory_tree: Dict[str, Union[Dict, Generator, None]] = {}
        current = directory_tree  # We will use current to build the inner dicts within the tree

        for root, dirs, files in os.walk(dir_path):
            working_dir_path = root.replace(dir_path, "")

            # By comparing the path to the directory we started in with the path to where we are now,
            # we can navigate to the correct part of the tree to populate the next batch of files.
            if working_dir_path:
                current = directory_tree
                # We do not include the first item as it's an empty string
                for level in working_dir_path.split("/")[1:]:
                    current = current.setdefault(level)  # type: ignore[assignment]

            for directory in dirs:
                current[directory] = {}

            for file in files:
                if self.is_f90_file(file):
                    current[file] = self.parse_file(f"{root}/{file}")
                elif include_non_fortran:
                    current[file] = None

        return directory_tree

    def is_f90_file(self, file_name: str) -> bool:
        return file_name.endswith(".f90")
