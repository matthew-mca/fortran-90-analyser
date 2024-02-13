from file_data_models.directory import Directory
from tests.object_factory.py_faker import PY_FAKER


def random_directory(**kwargs) -> Directory:
    kwargs.setdefault("name", PY_FAKER.pystr())

    return Directory(**kwargs)
