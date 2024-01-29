"""
The (currently) main entry point for the Fortran 90 code analyser.

Below is a list of the current commands available, as well as their arguments:

print-to-console: Prints the raw contents of a specified file.
    file-path: The full path to the file you wish to print to the console.
get-summary: Prints out a count of the different types of code blocks found in a file/codebase.
    code-path: The full path to the codebase/file you wish to parse.

"""
import os

import click

from code_data_models.fortran_function import FortranFunction
from code_data_models.fortran_interface import FortranInterface
from code_data_models.fortran_module import FortranModule
from code_data_models.fortran_program import FortranProgram
from code_data_models.fortran_subroutine import FortranSubroutine
from code_data_models.fortran_type import FortranType
from parsers.file_parser import FileParser


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option(
    "--file-path",
    required=True,
    prompt=True,
    help="The full path to the file you wish to print to the console.",
)
def print_to_console(file_path: str) -> None:
    file_parser = FileParser()
    try:
        for line in file_parser.parse_file_contents(file_path):
            click.echo(line, nl=False)
    except FileNotFoundError:
        click.echo("Unable to print file contents - the file path you have provided is not valid.")
    except Exception:
        click.echo("An unknown error occurred when attempting to read the file.")


@cli.command()
@click.option(
    "--code-path",
    required=True,
    prompt=True,
    help="The full path to the codebase/file you wish to parse.",
)
def get_summary(code_path: str) -> None:
    if not os.path.exists(code_path):
        click.echo("There was an error getting metrics: path is not valid.")
        return

    parser = FileParser()
    if os.path.isdir(code_path):
        codebase = parser.build_directory_tree(code_path)
        fortran_files = codebase.get_all_fortran_files()
    else:
        fortran_files = [parser.parse_file(code_path)]

    fortran_file_count = len(fortran_files)
    comment_count = 0
    function_count = 0
    interface_count = 0
    module_count = 0
    program_count = 0
    subroutine_count = 0
    type_count = 0

    for f90_file in fortran_files:
        comment_count += len([line for line in f90_file.contents if line.contains_comment])

        for component in f90_file.components:
            if isinstance(component, FortranFunction):
                function_count += 1
            if isinstance(component, FortranInterface):
                interface_count += 1
            if isinstance(component, FortranModule):
                module_count += 1
            elif isinstance(component, FortranProgram):
                program_count += 1
            if isinstance(component, FortranSubroutine):
                subroutine_count += 1
            elif isinstance(component, FortranType):
                type_count += 1

    click.echo("Codebase parsed...")
    click.echo()
    click.echo(f"# of Fortran 90 files: {fortran_file_count}")
    click.echo(f"# of Functions: {function_count}")
    click.echo(f"# of Interfaces: {interface_count}")
    click.echo(f"# of Modules: {module_count}")
    click.echo(f"# of Programs: {program_count}")
    click.echo(f"# of Subroutines: {subroutine_count}")
    click.echo(f"# of Derived Types: {type_count}")
    click.echo(f"# of Comments: {comment_count}")


if __name__ == "__main__":
    cli()
