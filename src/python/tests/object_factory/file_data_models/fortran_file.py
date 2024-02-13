from file_data_models.fortran_file import FortranFile
from tests.object_factory.py_faker import PY_FAKER


def random_fortran_file(**kwargs) -> FortranFile:
    kwargs.setdefault("path_from_root", PY_FAKER.pystr())
    kwargs.setdefault("contents", PY_FAKER.pylist(value_types=[str]))

    return FortranFile(**kwargs)
