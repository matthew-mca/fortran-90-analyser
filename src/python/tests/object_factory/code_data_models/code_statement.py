from code_data_models.code_statement import CodeStatement
from tests.object_factory.py_faker import PY_FAKER


def random_code_statement(**kwargs) -> CodeStatement:
    kwargs.setdefault("line_number", PY_FAKER.pyint())
    kwargs.setdefault("content", PY_FAKER.pystr())

    return CodeStatement(**kwargs)
