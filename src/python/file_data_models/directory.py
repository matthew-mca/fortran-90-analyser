from typing import Dict, List, Optional, Self, Union

from file_data_models import DigitalFile


class Directory:
    def __init__(self, name: str, subdirectories: List[Self] = [], files: List[DigitalFile] = []) -> None:
        self.name: str = name

        self.subdirectories: Dict[str, Self] = {}
        for subdir in subdirectories:
            self.subdirectories[subdir.name] = subdir

        self.files: Dict[str, DigitalFile] = {}
        for file_obj in files:
            self.files[file_obj.file_name] = file_obj

    def add_subdirectory(self, subdir: Self) -> None:
        if not self._name_is_taken(subdir.name):
            self.subdirectories[subdir.name] = subdir
        else:
            raise KeyError(f"Item with name '{subdir.name}' already exists inside of directory '{self.name}'.")

    def add_file(self, file_obj: DigitalFile) -> None:
        if not self._name_is_taken(file_obj.file_name):
            self.files[file_obj.file_name] = file_obj
        else:
            raise KeyError(f"Item with name '{file_obj.file_name}' already exists inside of directory '{self.name}'.")

    def get_item(self, key: str) -> Optional[Union[DigitalFile, Self]]:
        all_items = {}
        all_items.update(self.subdirectories)
        all_items.update(self.files)

        return all_items.get(key)

    def _name_is_taken(self, name: str) -> bool:
        all_names = list(self.subdirectories.keys()) + list(self.files.keys())

        if name in all_names:
            return True
        else:
            return False
