"""
The (currently) main entry point for the Fortran 90 code analyser.

Below is a list of the current commands available, as well as their
arguments:

get-raw-contents: Prints the raw contents of a specified file.
    file-path: The full path to the file you wish to print to the
      console.

get-summary: Prints out a count of the different types of code blocks
found in a file/codebase.
    code-path: The full path to the codebase/file you wish to parse.

list-all-variables: Prints a list of all Fortran files, the code blocks
they contain, and the variables those code blocks contain.
    code-path: The full path to the codebase/file you wish to parse.
"""

import os
from typing import Optional

import click

from code_data_models.code_block import CodeBlock
from code_data_models.fortran_function import FortranFunction
from code_data_models.fortran_interface import FortranInterface
from code_data_models.fortran_module import FortranModule
from code_data_models.fortran_program import FortranProgram
from code_data_models.fortran_subroutine import FortranSubroutine
from code_data_models.fortran_type import FortranType
from parsers.file_parser import FileParser
from serializers import SerializerRegistry


def check_output_path_file_extension(ctx: click.Context, param: click.Option, value: str) -> Optional[str]:
    if not (output_format := ctx.params["output_format"]):
        return None

    if value.endswith(f".{output_format}"):
        return value
    else:
        raise click.BadParameter(
            f"Output path must end with the extension for your chosen output format ({output_format})."
        )


@click.group()
@click.option(
    "--code-path",
    required=True,
    prompt=True,
    help="The full path to the codebase/file you wish to parse.",
    type=click.Path(exists=True, resolve_path=True),
)
@click.option(
    "--output-format",
    type=click.Choice(SerializerRegistry.get_all_serializable_formats(), case_sensitive=False),
    help="The format to serialize the results of a command to.",
    is_eager=True,
)
@click.option(
    "--output-path",
    help="The location to output the results of a command to.",
    callback=check_output_path_file_extension,
    type=click.Path(writable=True, resolve_path=True),
)
@click.pass_context
def cli(ctx: click.Context, code_path: str, output_format: str, output_path: str) -> None:
    ctx.ensure_object(dict)
    if (output_format and not output_path) or (output_path and not output_format):
        raise click.BadParameter(
            "A format and path must both be specified if outputting "
            "the results of your command to an alternative format."
        )

    parser = FileParser()
    if os.path.isdir(code_path):
        codebase = parser.build_directory_tree(code_path)
        fortran_files = codebase.get_all_fortran_files()
    else:
        fortran_files = [parser.parse_file(code_path)]

    if output_format:
        serializer = SerializerRegistry.get_serializer(output_format.lower(), output_path, fortran_files)
        ctx.obj["serializer"] = serializer
    else:
        ctx.obj["files"] = fortran_files


@cli.command()
@click.pass_context
def get_raw_contents(ctx: click.Context) -> None:
    if serializer := ctx.obj.get("serializer"):
        try:
            serializer.serialize_get_raw_contents()
            click.echo(f"Results serialized successfully to '{serializer.output_path}'.")
        except FileNotFoundError as e:
            click.echo(f"There was an error while serializing the result of get-raw-contents: {str(e)}")
        except Exception:
            click.echo("An unknown error occurred while serialzing the result of get-raw-contents.")

        return

    for f90_file in ctx.obj["files"]:
        click.echo(f90_file.file_name)
        for line in f90_file.contents:
            click.echo(f"\t{line.content}")


@cli.command()
@click.pass_context
def get_summary(ctx: click.Context) -> None:
    if serializer := ctx.obj.get("serializer"):
        try:
            serializer.serialize_get_summary()
            click.echo(f"Results serialized successfully to '{serializer.output_path}'.")
        except FileNotFoundError as e:
            click.echo(f"There was an error while serializing the result of get-summary: {str(e)}")
        except Exception:
            click.echo("An unknown error occurred while serialzing the result of get-summary.")

        return

    fortran_file_count = len(ctx.obj["files"])
    comment_count = 0
    function_count = 0
    interface_count = 0
    module_count = 0
    program_count = 0
    subroutine_count = 0
    type_count = 0

    for f90_file in ctx.obj["files"]:
        comment_count += len([line for line in f90_file.contents if line.contains_comment])

        for component in f90_file.components:
            if isinstance(component, FortranFunction):
                function_count += 1
            elif isinstance(component, FortranInterface):
                interface_count += 1
            elif isinstance(component, FortranModule):
                module_count += 1
            elif isinstance(component, FortranProgram):
                program_count += 1
            elif isinstance(component, FortranSubroutine):
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


@cli.command()
@click.option(
    "--no-duplicates",
    help=(
        "Stops variables found in the subprograms for a larger "
        "program unit from appearing more than once. Variables "
        "inside of any subprograms are only listed as part of the "
        "subprogram's variables, and not as part of the larger program "
        "unit's variables."
    ),
    is_flag=True,
)
@click.pass_context
def list_all_variables(ctx: click.Context, no_duplicates: bool) -> None:
    if serializer := ctx.obj.get("serializer"):
        try:
            serializer.serialize_list_all_variables(no_duplicates)
            click.echo(f"Results serialized successfully to '{serializer.output_path}'.")
        except FileNotFoundError as e:
            click.echo(f"There was an error while serializing the result of list-all-variables: {str(e)}")
        except Exception:
            click.echo("An unknown error occurred while serialzing the result of list-all-variables.")

        return

    def print_component_info(component: CodeBlock, indent_level: int = 0) -> None:
        indent = "\t" * indent_level

        class_name = type(component).__name__
        block_type = class_name.replace("Fortran", "")
        has_subprograms = getattr(component, "subprograms", []) != []

        component_info = ""

        if getattr(component, "is_recursive", None):
            component_info += f"Recursive {block_type.lower()} "
        else:
            component_info += f"{block_type} "

        if block_name := getattr(component, "block_name", None):
            component_info += f"'{block_name}' "

        component_info += f"from line {component.start_line_number} to {component.end_line_number};"

        click.echo(f"{indent}\t{component_info}")

        if hasattr(component, "variables"):
            if has_subprograms and no_duplicates:
                variable_list = component.get_variables_not_in_subprograms()
            else:
                variable_list = component.variables

            if variable_list:
                click.echo(f"{indent}\tVARIABLES")
                for var in variable_list:
                    click.echo(f"{indent}\t\t{var.data_type} '{var.name}' declared on line {var.line_declared};")

                click.echo()

        if has_subprograms:
            click.echo(f"{indent}\tSUBPROGRAMS")
            for subprogram in component.subprograms:
                print_component_info(subprogram, indent_level + 1)

    fortran_files = ctx.obj["files"]
    click.echo(f"Number of files found: {len(fortran_files)}")
    click.echo()

    for f90_file in fortran_files:
        click.echo(f"File path: '{f90_file.path_from_root}'")
        click.echo(f"Number of components in file: {len(f90_file.components)}")
        click.echo("Components in file:")

        for component in f90_file.components:
            print_component_info(component)
            click.echo()


if __name__ == "__main__":
    cli(obj={})
