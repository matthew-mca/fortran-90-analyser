"""
The (currently) main entry point for the Fortran 90 code analyser.

Below is a list of the current commands available, as well as their arguments:

print-to-console: Prints the raw contents of a specified file.
    file-path: The full path to the file you wish to print to the console.

"""
import click

from fortran_parser import parse_file


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
    try:
        for line in parse_file(file_path):
            click.echo(line, nl=False)
    except FileNotFoundError:
        click.echo(
            "Unable to print file contents - the file path you have provided is not valid."
        )
    except Exception:
        click.echo("An unknown error occurred when attempting to read the file.")


if __name__ == "__main__":
    cli()
