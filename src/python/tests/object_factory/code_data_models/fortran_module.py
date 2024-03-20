from code_data_models.fortran_module import FortranModule
from tests.object_factory.code_data_models.code_statement import random_code_statement
from tests.object_factory.code_data_models.fortran_function import random_fortran_function
from tests.object_factory.code_data_models.fortran_subroutine import random_fortran_subroutine
from tests.object_factory.py_faker import PY_FAKER


def random_fortran_module(**kwargs) -> FortranModule:
    kwargs.setdefault("parent_file_path", PY_FAKER.pystr())
    kwargs.setdefault(
        "contents",
        sorted(
            [random_code_statement() for _ in range(PY_FAKER.pyint(1, 50))],
            key=lambda statement: statement.line_number,
        ),
    )
    random_functions = [random_fortran_function() for _ in range(PY_FAKER.pyint(0, 5))]
    random_subroutines = [random_fortran_subroutine() for _ in range(PY_FAKER.pyint(0, 5))]
    kwargs.setdefault("subprograms", random_functions + random_subroutines)

    return FortranModule(**kwargs)
