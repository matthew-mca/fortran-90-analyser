import os
from typing import Generator, Union

from file_data_models.digital_file import DigitalFile
from file_data_models.directory import Directory
from file_data_models.fortran_file import FortranFile


class FileParser:
    """Parses the content of files and directories."""

    def parse_file(self, file_path: str) -> Union[DigitalFile, FortranFile]:
        """Parses a file at a specified path and returns it as an object.

        Args:
            file_path: The path to the file.

        Returns:
            A file object. If the file is a Fortran file, its contents are also included.
        """

        file_name = file_path.split("/")[-1]

        if not self.is_f90_file(file_name):
            return DigitalFile(file_name)
        else:
            file_contents = self.parse_file_contents(file_path)
            return FortranFile(file_name, file_contents)

    def parse_file_contents(self, file_path: str) -> Generator[str, None, None]:
        """Parses the contents of the file at the specified path and yields its contents line by line.

        Args:
            file_path: The path to the file.

        Yields:
            Each individual line of the file.
        """

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
        """Builds out a representation of a specified directory.

        Args:
            dir_path: The path to the directory.
            include_non_fortran: A flag that determines whether any non-Fortran file objects are
              included in the final result.

        Returns:
            A directory populated with all the files and subdirectories of the directory the provided
            path points to.

        Raises:
            ValueError: The given path did not exist, or pointed to a file rather than a directory.
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
                if self.is_f90_file(file_name) or include_non_fortran:
                    new_file = self.parse_file(f"{root}/{file_name}")
                    current.add_file(new_file)

        return directory_tree

    def is_f90_file(self, file_name: str) -> bool:
        """Checks if a given file is a Fortran 90 file.

        Args:
            file_name: The name of the file.

        Returns:
            A boolean that is True if the file has a .f90 extension, otherwise False.
        """

        return file_name.endswith(".f90")
