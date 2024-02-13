from code_data_models.variable import Variable
from tests.object_factory.py_faker import PY_FAKER


def random_variable(**kwargs) -> Variable:
    kwargs.setdefault("data_type", PY_FAKER.pystr())
    kwargs.setdefault("attributes", PY_FAKER.pylist(value_types=[str]))
    kwargs.setdefault("name", PY_FAKER.pystr())
    kwargs.setdefault("parent_file_path", PY_FAKER.pystr())
    kwargs.setdefault("line_declared", PY_FAKER.pyint())
    kwargs.setdefault("possibly_unused", PY_FAKER.pybool())

    return Variable(**kwargs)
