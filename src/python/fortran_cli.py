"""
The main entry point for the Fortran 90 code analyser.

In order to view information about the available CLI commands and their
various options, run this file with the --help flag. It is also possible
to view information about a specific command by running the command with
the --help flag.

Further information on how to use the CLI is available in the project's
README file. There is also information on the format of the JSON and
YAML serializer outputs available in the 'docs' directory at the root of
the project.
"""

import os
import tomllib
from collections import defaultdict
from configparser import ConfigParser
from typing import Any, Dict

import click

from code_data_models.code_block import CodeBlock
from code_data_models.variable import Variable
from file_data_models.fortran_file import FortranFile
from parsers.file_parser import FileParser
from serializers import SerializerRegistry


def check_output_path_file_extension(output_format: str, output_path: str) -> None:
    if (output_format and not output_path) or (output_path and not output_format):
        raise click.BadParameter(
            "A format and path must both be specified if outputting "
            "the results of your command to an alternative format."
        )

    if not output_path.endswith(f".{output_format}"):
        raise click.BadParameter(
            f"Output path must end with the extension for your chosen output format ({output_format})."
        )


def read_from_config(ctx: click.Context, param: click.Option, config_path: str | None) -> None:
    if config_path is None:
        return

    if config_path.endswith("toml"):
        ctx.default_map = _read_toml_config(config_path)
    elif config_path.endswith("ini"):
        ctx.default_map = _read_ini_config(config_path)
    else:
        raise click.BadParameter("Config file must be of type TOML or INI.")


def _read_ini_config(config_path: str) -> dict[str, Any]:
    cfg = ConfigParser()
    cfg.read(config_path)
    ini_config: dict[str, Any] = {}

    for sect in cfg.sections():
        command_path = sect.split(".")
        if command_path[0] != "options":
            continue

        defaults = ini_config
        for command in command_path[1:]:
            defaults = defaults.setdefault(command, {})

        defaults.update(cfg[sect])

    return ini_config


def _read_toml_config(config_path: str) -> dict[str, Any]:
    with open(config_path, "rb") as f:
        toml_config: dict[str, Any] = tomllib.load(f)

    return toml_config["options"]


@click.group(
    epilog=(
        "For more information about the available CLI commands, please "
        "see the documentation available in the 'docs' directory."
    )
)
@click.option(
    "--code-path",
    envvar="FORTRAN_CODE_PATH",
    help="The full path to the codebase/file you wish to parse.",
    prompt=True,
    required=True,
    type=click.Path(exists=True, resolve_path=True),
)
@click.option(
    "--output-format",
    envvar="OUTPUT_FORMAT",
    help="The format to serialize the results of a command to.",
    type=click.Choice(SerializerRegistry.get_all_serializable_formats(), case_sensitive=False),
)
@click.option(
    "--output-path",
    envvar="OUTPUT_PATH",
    help="The location to output the serializer's results to.",
    type=click.Path(writable=True, resolve_path=True),
)
@click.option(
    "--config",
    callback=read_from_config,
    envvar="CLI_CONFIG_PATH",
    expose_value=False,
    help=(
        "The path to a config file containing default values for the "
        "various CLI options. Accepts both INI and TOML formats."
    ),
    is_eager=True,
    show_default=True,
    type=click.Path(dir_okay=False),
)
@click.option(
    "--fortran-only",
    envvar="FORTRAN_ONLY",
    help="Excludes non-FORTRAN files from parsing.",
    is_flag=True,
)
@click.pass_context
def cli(ctx: click.Context, code_path: str, output_format: str, output_path: str, fortran_only: bool) -> None:
    ctx.ensure_object(dict)
    if output_format or output_path:
        check_output_path_file_extension(output_format, output_path)

    parser = FileParser()
    if os.path.isdir(code_path):
        codebase = parser.build_directory_tree(code_path, fortran_only)
        collected_files = codebase.get_all_files()
    else:
        collected_files = [parser.parse_file(code_path)]

    if output_format:
        serializer = SerializerRegistry.get_serializer(output_format.lower(), output_path, collected_files)
        ctx.obj["serializer"] = serializer
    else:
        ctx.obj["files"] = collected_files

    file_count = len(collected_files)
    failed_parse_count = sum(item.failed_fortran_parse for item in collected_files)
    fortran_file_count = sum(isinstance(item, FortranFile) for item in collected_files) + failed_parse_count

    click.echo()
    click.echo("Codebase parsed. \n")
    click.echo(f"# of files: {file_count}")
    click.echo(f"# of FORTRAN files: {fortran_file_count}")
    click.echo(f"# of FORTRAN files that failed parsing: {failed_parse_count}")
    click.echo()


@cli.command(short_help="Obtains the raw contents of the found Fortran file(s).")
@click.pass_context
def get_raw_contents(ctx: click.Context) -> None:
    if serializer := ctx.obj.get("serializer"):
        try:
            serializer.serialize_get_raw_contents()
            click.echo(f"Results serialized successfully to '{serializer.output_path}'.")
        except FileNotFoundError as e:
            click.echo(f"There was an error while serializing the result of get-raw-contents: {str(e)}")
        except Exception:
            click.echo("An unknown error occurred while serializing the result of get-raw-contents.")

        return

    for file_obj in ctx.obj["files"]:
        click.echo(f"> {file_obj.path_from_root}")
        if isinstance(file_obj, FortranFile):
            for line in file_obj.contents:
                click.echo(f"\t{line.content}")
        click.echo()


@cli.command(short_help="Counts the amount of code blocks, variables and comments in the found Fortran file(s).")
@click.option(
    "--top-level-blocks",
    envvar="TOP_LEVEL_BLOCKS",
    help="Does not include subprogram information in the summary.",
    is_flag=True,
)
@click.option(
    "--top-level-vars",
    envvar="TOP_LEVEL_VARS",
    help=(
        "Does not include variable information for variables that are "
        "found in a program unit's subprograms in the summary. This "
        "flag has no effect if --top-level-blocks is not set."
    ),
    is_flag=True,
)
@click.pass_context
def get_summary(ctx: click.Context, top_level_blocks: bool, top_level_vars: bool) -> None:
    if serializer := ctx.obj.get("serializer"):
        try:
            serializer.serialize_get_summary(top_level_blocks, top_level_vars)
            click.echo(f"Results serialized successfully to '{serializer.output_path}'.")
        except FileNotFoundError as e:
            click.echo(f"There was an error while serializing the result of get-summary: {str(e)}")
        except Exception:
            click.echo("An unknown error occurred while serializing the result of get-summary.")

        return

    comment_count = 0
    found_blocks = []
    found_variables = []

    for file_obj in ctx.obj["files"]:
        if isinstance(file_obj, FortranFile):
            found_blocks.extend(file_obj.components)
            comment_count += sum(line.contains_comment for line in file_obj.contents)

    if not top_level_blocks:
        subprograms = []
        for code_block in found_blocks:
            subprograms.extend(code_block.get_all_subprograms())

        found_blocks.extend(subprograms)

    if not top_level_blocks or top_level_vars:
        for block in found_blocks:
            if hasattr(block, "variables") and hasattr(block, "subprograms"):
                found_variables.extend(block.get_variables_not_in_subprograms())
    else:
        for block in found_blocks:
            if hasattr(block, "variables"):
                found_variables.extend(block.variables)

    block_counts: Dict[str, int] = defaultdict(int)
    for block in found_blocks:
        class_name = type(block).__name__
        block_counts[class_name] += 1

    variable_counts = {}
    for var_type in Variable.ALL_DATA_TYPES:
        # We do 'in' instead of '==' here since some data types can have
        # extra information as part of the type declaration, e.g
        # 'INTEGER(I8)'.
        variable_counts[var_type] = sum(var_type in var.data_type for var in found_variables)

    click.echo(f"# of comments: {comment_count}")

    CODE_BLOCK_KEYS = [
        "FortranDoLoop",
        "FortranFunction",
        "FortranIfBlock",
        "FortranInterface",
        "FortranModule",
        "FortranProgram",
        "FortranSubroutine",
        "FortranType",
    ]

    click.echo("\nCode blocks found:")
    for block_type in CODE_BLOCK_KEYS:
        click.echo(f"\t{block_type}: {block_counts[block_type]}")

    click.echo("\nVariables found:")
    for var_type, count in variable_counts.items():
        click.echo(f"\t{var_type}: {count}")


@cli.command(short_help="Lists all the variables in the found Fortran file(s).")
@click.option(
    "--no-duplicates",
    envvar="NO_DUPLICATE_VARS",
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
            click.echo("An unknown error occurred while serializing the result of list-all-variables.")

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

    collected_files = ctx.obj["files"]

    for file_obj in collected_files:
        is_fortran_file = isinstance(file_obj, FortranFile) or file_obj.failed_fortran_parse
        initial_message = "> FORTRAN file" if is_fortran_file else "> File"
        initial_message += f" '{file_obj.path_from_root}'"
        if file_obj.failed_fortran_parse:
            initial_message += "\n\tFile parse failed during collection."
        if not isinstance(file_obj, FortranFile):
            initial_message += "\n"

        click.echo(initial_message)

        if isinstance(file_obj, FortranFile):
            click.echo(f"> Number of components in file: {len(file_obj.components)}")
            click.echo("> Components in file:")
            for component in file_obj.components:
                print_component_info(component)
                click.echo()


if __name__ == "__main__":
    cli(obj={})
