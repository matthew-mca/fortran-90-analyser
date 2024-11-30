# FORTRAN CLI Options Usage Info

The following guide provides information about how passing options to the CLI works. Information
about the specific commands and options themselves is available by running the `fortran_cli.py` file
with the `--help` flag.

When running the CLI and passing options via the command line, there are options that are provided
prior to specifying a command name. These are the options common to all the commands in the
application. Any options unique to a specific command are provided *after* specifying the command
name. You can also provide options to the CLI using environment variables or a config file.

## The Hierarchy of CLI Options

Options can be provided to the CLI in three ways:

1. Providing options on the command line when specifying a command,
2. Environment variables,
3. A `.ini` config file.

The above order is also the order in which the CLI checks for an option's value, with options
provided on the command line taking precedent over the other two inputs.

## Environment Variables

The following list details the environment variable names for all of the options in the application:

- **code-path:** `FORTRAN_CODE_PATH`
- **output-format:** `OUTPUT_FORMAT`
- **output-path:** `OUTPUT_PATH`
- **fortran-only:** `FORTRAN_ONLY`
- **top-level-blocks:** `TOP_LEVEL_BLOCKS`
- **top-level-vars:** `TOP_LEVEL_VARS`
- **config:** `CLI_CONFIG_PATH`
- **no-duplicates:** `NO_DUPLICATE_VARS`

There is also an environment variable called `ADDITIONAL_FORTRAN_EXTENSIONS_BETA`, that will parse FORTRAN files with
the `.f`, `.F`, and `.F90` extensions when it is set to the string value `"true"`. Reading of `.F`/`.f` files in
particular is not as stable as reading `.f90` files, so be mindful that parsing these extra file formats may result in
additional parsing failures!

## Config Files

It is possible to provide options to the CLI via a `.ini` or `.toml` configuration file. The path to the file
can be provided using the CLI's `--config` option, or the environment variable `CLI_CONFIG_PATH`.

The base options that are required for *every* command are listed under a section titled `options`.
Options specific to a certain command are listed under a section with the title format
`options.command`, where `command` is the name of the command. The names of the settings in the
config file are the same as the names of the flags in the CLI, with the only difference being the
hyphens (`-`) are instead underscores (`_`).

Below is an example that shows the format of both a `.ini` and `.toml` config file for the
application:

### INI Config
```ini
[options]
code_path = .
output_format = json
output_path = ./results.json
fortran_only = true

[options.get-summary]
top_level_blocks = true
top_level_vars = false

[options.list-all-variables]
no_duplicates = true
```

### TOML Config
```toml
[options]
code_path = "."
output_format = "json"
output_path = "./results.json"
fortran_only = true

[options.get-summary]
top_level_blocks = true
top_level_vars = false

[options.list-all-variables]
no_duplicates = true
```
