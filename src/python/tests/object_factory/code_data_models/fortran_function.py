from code_data_models.fortran_function import FortranFunction
from tests.object_factory.code_data_models.code_statement import random_code_statement
from tests.object_factory.code_data_models.fortran_do_loop import random_fortran_do_loop
from tests.object_factory.code_data_models.fortran_if_block import random_fortran_if_block
from tests.object_factory.py_faker import PY_FAKER


def random_fortran_function(**kwargs) -> FortranFunction:
    kwargs.setdefault("parent_file_path", PY_FAKER.pystr())
    kwargs.setdefault(
        "contents",
        sorted(
            [random_code_statement() for _ in range(PY_FAKER.pyint(1, 50))],
            key=lambda statement: statement.line_number,
        ),
    )
    random_do_loops = [random_fortran_do_loop() for _ in range(PY_FAKER.pyint(0, 5))]
    random_if_blocks = [random_fortran_if_block() for _ in range(PY_FAKER.pyint(0, 5))]
    kwargs.setdefault("subprograms", random_do_loops + random_if_blocks)

    return FortranFunction(**kwargs)
