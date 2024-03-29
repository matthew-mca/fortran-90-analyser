from code_data_models.fortran_do_loop import FortranDoLoop
from tests.object_factory.code_data_models.code_statement import random_code_statement
from tests.object_factory.py_faker import PY_FAKER


def random_fortran_do_loop(**kwargs) -> FortranDoLoop:
    kwargs.setdefault("parent_file_path", PY_FAKER.pystr())
    kwargs.setdefault(
        "contents",
        sorted(
            [random_code_statement() for _ in range(PY_FAKER.pyint(1, 50))],
            key=lambda statement: statement.line_number,
        ),
    )
    kwargs.setdefault("subprograms", [])

    return FortranDoLoop(**kwargs)