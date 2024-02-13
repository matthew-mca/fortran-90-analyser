from file_data_models.digital_file import DigitalFile
from tests.object_factory.py_faker import PY_FAKER


def random_digital_file(**kwargs) -> DigitalFile:
    kwargs.setdefault("path_from_root", PY_FAKER.pystr())

    return DigitalFile(**kwargs)
