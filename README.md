# A Python-based Code Analyser for Fortran 90

This project aims to use the language Python to develop a code analysis tool for the programming
language [Fortran 90](https://en.wikipedia.org/wiki/Fortran).

This project is being undertaken as part of the final year of my Computer Science degree, under the
supervision of [Professor Austen Rainer](https://pure.qub.ac.uk/en/persons/austen-rainer). The end
goal of the project is to be able to parse Fortran 90 files or entire codebases and report back
metrics to the user about their code.

## Table of Contents

- [Installation](https://gitlab.eeecs.qub.ac.uk/40291992/fortran-90-analyser#installation)
- [Usage](https://gitlab.eeecs.qub.ac.uk/40291992/fortran-90-analyser#usage)
- [Roadmap](https://gitlab.eeecs.qub.ac.uk/40291992/fortran-90-analyser#roadmap)
- [Contributing](https://gitlab.eeecs.qub.ac.uk/40291992/fortran-90-analyser#contributing)
- [Support](https://gitlab.eeecs.qub.ac.uk/40291992/fortran-90-analyser#support)
- [Acknowledgements](https://gitlab.eeecs.qub.ac.uk/40291992/fortran-90-analyser#acknowledgements)

## Installation

Currently, the project installation is simply
[cloning the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
and installing any required dependencies, as well as the correct version of Python. This project is
built on version `3.11.2` of Python.

### Requirements

Any dependencies needed for the project are listed in the `requirements.txt` and
`requirements-dev.txt` files, which themselves are compiled using their respective `.in` files and
the library `pip-tools`. It is recommended to
[create a virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments)
for the project before installing any dependencies.

Use the following command in your terminal to install these dependencies: 

```
pip3 install -r requirements.txt -r requirements-dev.txt
```

Alternatively, install `pip-tools` directly and use the included `pip-sync` command to
install/upgrade/uninstall everything necessary to match the requirements:

```
pip3 install pip-tools
pip-sync requirements.txt requirements-dev.txt
```

## Usage

The project is CLI-based, the source code for which is available in the `fortran_cli.py` file. In
order to use it, run the file as a regular Python file, supplying whatever commands/subcommands and
options needed.

This is what it looks like from the root of the project:

```
python3 src/python/fortran_cli.py <commands/options>
```

To show an example, we will use the first command ever added to the analyser, `get-raw-contents`.
This command takes the path to a Fortran 90 file and simply outputs its raw contents. There are
certain options common to every command that are provided *before* specifying a command name, rather
than after. The `--code-path` option is currently the one common option that is ***required*** in
order to run a CLI command.

So following the above format, an example run of this command looks like:

```bash
python3 src/python/fortran_cli.py --code-path /Users/testuser/fortran/hello_world.f90 get-raw-contents
```

For a simple hello world program, the output to the terminal would look like the following:

```
PROGRAM hello_world
    PRINT *, "Hello World!"
END PROGRAM hello_world
```

Success! We ran a command using the CLI.

It is also possible to output the results of a command to a file, rather than simply printing it to
the console. This is done by passing the `--output-format` and `--output-path` options when running
a command. The two formats currently supported are JSON and YAML. Information on the structure of
the JSON and YAML outputs is available in the
[serialiser-output-structure.md file](./docs/serialiser-output-structure.md).

This file uses the library [Click](https://click.palletsprojects.com/en/8.1.x/#) to build its CLI
capability. For a list of all the commands and options available in the application, simply run the
`fortran_cli.py` file with the `--help` flag. There is also information available on the different
ways to provide input to the application available in the
[cli-options-usage.md file](./docs/cli-options-usage.md).

## Roadmap

As of the most recent version of this README, the project is nearing its deadline, at which point it
will be assessed as part of my final year of university. There are then plans to make this
application available to users who have a FORTRAN codebase available for scanning.

It is likely this project will also be put up on a public GitHub repository and will be looking for
contributors once the project has been assessed, but this is unconfirmed. This section, as well as
the `Contributing` section, will be updated as soon as more information is available.

## Contributing

While there are potential plans to make this tool available after finishing the project, currently
the project's code is not available to others for editing yet. Any and all additions or changes in
the project are made exclusively by myself.

## Support

Find any problems with the application?
[Create an issue in the project's GitLab repo](https://gitlab.eeecs.qub.ac.uk/40291992/fortran-90-analyser/-/issues/new).
Please be mindful to follow the template provided in the issue description.

## Acknowledgements

This project would not be possible without the help of
[Professor Austen Rainer](https://pure.qub.ac.uk/en/persons/austen-rainer) and
[Doctor David Cutting](https://pure.qub.ac.uk/en/persons/david-cutting). Their guidance and support
have been and continue to be instrumental in the development of this code analyser.

I would also like to extend a thanks to the entirety of the InsightCloudSec team in Rapid7. The 15
months I spent on placement as an engineer in their Coverage and Analysis team taught me many things
about not just Python, but the wider world of software development. The experience has undoubtedly
made a huge difference to my final year!

There is live test data in use as part of the integration testing in the project, all of which has
been taken straight from GitHub. A list of the repositories used (as well as their authors) is
available below:

- [Fortran](https://github.com/TheAlgorithms/Fortran) by
  [The Algorithms](https://github.com/TheAlgorithms/).

These repositories allow for testing of the application on *real Fortran code*, so thank you all!

***

**Project Owner:** *[Matthew McAteer](https://github.com/matthew-mca)*

**Last Updated:** *28/03/2024*