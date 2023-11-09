import os
from typing import Generator, Union

from file_data_models import *


class FortranParser:
    def parse_file(self, file_path: str) -> Union[DigitalFile, FortranFile]:
        file_name = file_path.split("/")[-1]

        if not self.is_f90_file(file_name):
            return DigitalFile(file_name)
        else:
            file_contents = self.parse_file_contents(file_path)
            return FortranFile(file_name, file_contents)

    def parse_file_contents(self, file_path: str) -> Generator[str, None, None]:
        with open(file_path, "r") as f:
            line = f.readline()
            while line:
                yield line
                line = f.readline()

    def build_directory_tree(
        self,
        dir_path: str,
        include_non_fortran: bool = True,
    ) -> Directory:
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

        root_dir_name = dir_path.split("/")[-1]
        directory_tree: Directory = Directory(root_dir_name)
        current = directory_tree  # We will use current to build the inner dicts within the tree

        for root, dirs, files in os.walk(dir_path):
            working_dir_path = root.replace(dir_path, "")

            # By comparing the path to the directory we started in with the path to where we are now,
            # we can navigate to the correct part of the tree to populate the next batch of files.
            if working_dir_path:
                current = directory_tree
                # We do not include the first item as it's an empty string
                for level in working_dir_path.split("/")[1:]:
                    current = current.get_item(level)  # type: ignore[assignment]

            for directory_name in dirs:
                new_directory = Directory(directory_name)
                current.add_subdirectory(new_directory)

            for file_name in files:
                new_file = self.parse_file(f"{root}/{file_name}")
                current.add_file(new_file)

        return directory_tree

    def is_f90_file(self, file_name: str) -> bool:
        return file_name.endswith(".f90")
