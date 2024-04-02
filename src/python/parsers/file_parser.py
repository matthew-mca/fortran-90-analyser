import logging
import os
from pathlib import PurePath
from typing import Generator, Optional, Union

from file_data_models.digital_file import DigitalFile
from file_data_models.directory import Directory
from file_data_models.fortran_file import FortranFile

logger = logging.getLogger("FILE_PARSER")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("| [%(levelname)s] %(asctime)s | %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler("file_parser_errors.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

file_handler2 = logging.FileHandler("file_parser.log")
file_handler2.setLevel(logging.INFO)
file_handler2.setFormatter(formatter)
logger.addHandler(file_handler2)


class FileParser:
    """Parses the content of files and directories."""

    def parse_file(self, file_path: str, root_dir_path: Optional[str] = None) -> Union[DigitalFile, FortranFile]:
        """Parses a file at a given path and returns it as an object.

        Args:
            file_path: The path to the file.
            root_dir_path: The path to the root of the codebase being
              parsed. If there is no root directory path provided, this
              value is defaulted to the absolute path to the file.

        Returns:
            A file object. If the file is a Fortran file, its contents
            are also included.
        """

        if root_dir_path:
            path_from_root_dir = file_path.replace(root_dir_path, "")
        else:
            path_from_root_dir = os.path.abspath(file_path)

        if self.is_f90_file(file_path):
            logger.info("Parsing FORTRAN file '%s'...", path_from_root_dir)
            file_contents = self.parse_file_contents(file_path)
            try:
                new_file = FortranFile(path_from_root_dir, file_contents)
            except Exception as e:
                if os.environ.get("RAISE_PARSING_ERRORS", "").lower() == "true":
                    raise e

                logger.error(
                    "Something went wrong while parsing FORTRAN file '%s'. Storing minimal data.",
                    path_from_root_dir,
                )
                new_file = DigitalFile(path_from_root_dir, failed_fortran_parse=True)
        else:
            logger.info("Parsing file '%s'...", path_from_root_dir)
            new_file = DigitalFile(path_from_root_dir)

        return new_file

    def parse_file_contents(self, file_path: str) -> Generator[str, None, None]:
        """Parses the contents of the file.

        Parses the contents of the file, and then yields the contents
        line by line.

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
        dir_path: Union[str, PurePath],
        fortran_only: bool = True,
    ) -> Directory:
        """Builds out a representation of a specified directory.

        Args:
            dir_path: The path to the directory.
            fortran_only: A flag that determines whether any non-Fortran
              file objects are included in the final result.

        Returns:
            A directory populated with all the files and subdirectories
            of the directory the provided path points to.

        Raises:
            ValueError: The given path did not exist, or pointed to a
              file rather than a directory.
        """

        # Will resolve relative paths and leave absolute paths as is.
        dir_path = PurePath(os.path.abspath(dir_path))

        if not os.path.exists(dir_path):
            raise ValueError("Given path does not exist.")
        elif os.path.isfile(dir_path):
            raise ValueError("Specified path is a file, not a directory.")

        root_dir_name = dir_path.parts[-1]
        directory_tree: Directory = Directory(root_dir_name)
        current = directory_tree  # We will use current to build the inner dicts within the tree

        for root, dirs, files in os.walk(dir_path):
            working_dir_path = PurePath(root.replace(str(dir_path), ""))

            # By comparing the path to the directory we started in with
            # the path to where we are now, we can navigate to the
            # correct part of the tree to populate the next batch of
            # files.
            if working_dir_path:
                current = directory_tree
                # We do not include the first item as it's not any sort
                # of directory name
                for level in working_dir_path.parts[1:]:
                    current = current.get_item(level)  # type: ignore[assignment]

            for directory_name in dirs:
                new_directory = Directory(directory_name)
                current.add_subdirectory(new_directory)

            for file_name in files:
                if self.is_f90_file(file_name) or not fortran_only:
                    new_file = self.parse_file(os.path.join(root, file_name), str(dir_path))
                    current.add_file(new_file)

        return directory_tree

    def is_f90_file(self, file_path: str) -> bool:
        """Checks if a given file is a Fortran 90 file.

        Args:
            file_path: The path to the file.

        Returns:
            A boolean that is True if the file has a valid FORTRAN
            extension, otherwise False.
        """

        valid_f90_extensions = [".f90"]
        # Some of these file extensions are more unstable than standard
        # lowercase .f90
        if os.environ.get("ADDITIONAL_FORTRAN_EXTENSIONS_BETA", "") == "true":
            valid_f90_extensions.extend([".f", ".F90", ".F"])

        return any(file_path.endswith(extension) for extension in valid_f90_extensions)
