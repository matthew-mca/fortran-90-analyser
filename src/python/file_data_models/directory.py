from typing import Dict, List, Optional, Self, Union

from utils.repr_builder import build_repr_from_attributes

from .digital_file import DigitalFile


class Directory:
    """A computer directory that can contain both files and subdirectories.

    Attributes:
        name: The name of the directory.
        subdirectories: A dict of directories, where the key is the name of the directory.
        files: A dict of files, where the key is the name of the file.
    """

    def __init__(self, name: str, subdirectories: List[Self] = [], files: List[DigitalFile] = []) -> None:
        """Initialises a directory object and populates it with the provided subdirectories and files.

        Args:
            name: The name of the directory.
            subdirectories: A list of subdirectories to include in the directory.
            files: A list of files to include in the directory.
        """

        self.name: str = name

        self.subdirectories: Dict[str, Self] = {}
        for subdir in subdirectories:
            self.subdirectories[subdir.name] = subdir

        self.files: Dict[str, DigitalFile] = {}
        for file_obj in files:
            self.files[file_obj.file_name] = file_obj

    def add_subdirectory(self, subdir: Self) -> None:
        """Adds a provided directory into the directory object.

        Args:
            subdir: The directory object to be added.

        Raises:
            KeyError: An item with the same name as the provided directory already exists in the directory.
        """

        if not self._name_is_taken(subdir.name):
            self.subdirectories[subdir.name] = subdir
        else:
            raise KeyError(f"Item with name '{subdir.name}' already exists inside of directory '{self.name}'.")

    def add_file(self, file_obj: DigitalFile) -> None:
        """Adds a provided file into the directory object.

        Args:
            file_obj: The file object to be added.

        Raises:
            KeyError: An item with the same name as the provided file already exists in the directory.
        """

        if not self._name_is_taken(file_obj.file_name):
            self.files[file_obj.file_name] = file_obj
        else:
            raise KeyError(f"Item with name '{file_obj.file_name}' already exists inside of directory '{self.name}'.")

    def get_item(self, key: str) -> Optional[Union[DigitalFile, Self]]:
        """Returns an item with the provided key from the directory, or None if no such item exists.

        Args:
            key: The name of the item to look for in the directory.

        Returns:
            A file or subdirectory with the same name as the provided key, or None.
        """

        all_items = {}
        all_items.update(self.subdirectories)
        all_items.update(self.files)  # type: ignore[arg-type]

        return all_items.get(key)

    def _name_is_taken(self, name: str) -> bool:
        """Checks for the existence of a given name in the directory."""

        all_names = list(self.subdirectories.keys()) + list(self.files.keys())

        if name in all_names:
            return True
        else:
            return False

    def __repr__(self) -> str:
        return build_repr_from_attributes(
            class_name=type(self).__name__,
            name=self.name,
            files=len(self.files),
            subdirectories=len(self.subdirectories),
        )
