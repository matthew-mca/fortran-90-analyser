import json
import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from fortran_cli import cli


class TestFortranCLI:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def configured_runner(self, live_data_path):
        return CliRunner(env={"FORTRAN_CODE_PATH": live_data_path, "FORTRAN_ONLY": "true"})

    @pytest.fixture
    def live_data_path(self):
        return os.path.abspath("./src/python/tests/integration/.live_test_data/Fortran")

    def test_check_output_path_file_extension(self, runner, live_data_path):
        expected_error_message = (
            "A format and path must both be specified if outputting "
            "the results of your command to an alternative format."
        )

        # Output format with no output path
        result = runner.invoke(cli, ["--code-path", live_data_path, "--output-format", "json", "get-summary"])

        assert result.exit_code == 2
        assert expected_error_message in result.output

        # Output path with no output format
        result = runner.invoke(cli, ["--code-path", live_data_path, "--output-path", ".", "get-summary"])

        assert result.exit_code == 2
        assert expected_error_message in result.output

        # Both options supplied, but the file extension of the file in
        # the output path does not match the output format chosen.
        expected_error_message = (
            "Invalid value: Output path must end with the extension for your chosen output format (json)."
        )
        result = runner.invoke(
            cli,
            [
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                "./incorrect_extension.txt",
                "get-summary",
            ],
        )

        assert result.exit_code == 2
        assert expected_error_message in result.output

    def test_fortran_cli_unsupported_output_format(self, runner, live_data_path):
        expected_error_message = "Error: Invalid value for '--output-format': 'txt' is not one of 'json', 'yaml'."
        result = runner.invoke(
            cli,
            [
                "--code-path",
                live_data_path,
                "--output-format",
                "txt",
                "--output-path",
                "./unsupported.txt",
                "get-summary",
            ],
        )

        assert result.exit_code == 2
        assert expected_error_message in result.output

    def test_fortran_cli_code_path_is_single_file(self, runner, live_data_path):
        live_file_path = live_data_path + "/simple_eg/hello_world.f90"
        result = runner.invoke(cli, ["--code-path", live_file_path, "get-raw-contents"])
        assert result.exit_code == 0

    def test_fortran_cli_environment_variables(self, live_data_path):
        env_runner = CliRunner(
            env={
                "FORTRAN_CODE_PATH": live_data_path,
                "FORTRAN_ONLY": "true",
            }
        )

        result = env_runner.invoke(cli, ["get-summary"])
        assert result.exit_code == 0
        assert "Codebase parsed." in result.output

    def test_fortran_cli_config_file(self, runner, live_data_path, tmp_path):
        config_path = tmp_path / "test_config.ini"
        output_path = tmp_path / "output.json"

        with open(config_path, "w") as f:
            f.write("[options]\n")
            f.write(f"code_path = {live_data_path}\n")
            f.write(f"output_path = {output_path}\n")
            f.write("output_format = json\n")
            f.write("fortran_only = true\n")
            f.write("\n")
            f.write("[options.get-summary]\n")
            f.write("top_level_blocks = true\n")
            f.write("top_level_vars = false\n")

        expected_output = "Results serialized successfully"
        result = runner.invoke(cli, ["--config", str(config_path), "get-summary"])

        assert result.exit_code == 0
        assert expected_output in result.output

        with open(output_path, "r") as f:
            data = json.load(f)

        assert data["topLevelCodeBlocksOnly"] is True
        assert data["topLevelVariablesOnly"] is False

    def test_get_raw_contents(self, configured_runner):
        result = configured_runner.invoke(cli, ["get-raw-contents"])
        assert result.exit_code == 0

    @patch("fortran_cli.SerializerRegistry.get_serializer")
    def test_get_raw_contents_file_not_found_error(self, mock_registry, runner, live_data_path):
        mock_registry.return_value.serialize_get_raw_contents.side_effect = FileNotFoundError
        result = runner.invoke(
            cli,
            [
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                "./output.json",
                "get-raw-contents",
            ],
        )
        expected_output = "There was an error while serializing the result of get-raw-contents"
        assert expected_output in result.output

    @patch("fortran_cli.SerializerRegistry.get_serializer")
    def test_get_raw_contents_generic_exception(self, mock_registry, runner, live_data_path):
        mock_registry.return_value.serialize_get_raw_contents.side_effect = Exception
        result = runner.invoke(
            cli,
            [
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                "./output.json",
                "get-raw-contents",
            ],
        )
        expected_output = "An unknown error occurred while serializing the result of get-raw-contents."
        assert expected_output in result.output

    def test_get_summary(self, configured_runner):
        result = configured_runner.invoke(cli, ["get-summary"])
        assert result.exit_code == 0

        expected_messages = [
            "Codebase parsed.",
            "# of files: 9",
            "# of FORTRAN files: 9",
            "# of FORTRAN files that failed parsing: 0",
            "# of comments: 108",
            "Code blocks found:",
            "Variables found:",
        ]
        for message in expected_messages:
            assert message in result.output

    @patch("fortran_cli.SerializerRegistry.get_serializer")
    def test_get_summary_file_not_found_error(self, mock_registry, runner, live_data_path):
        mock_registry.return_value.serialize_get_summary.side_effect = FileNotFoundError
        result = runner.invoke(
            cli,
            [
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                "./output.json",
                "get-summary",
            ],
        )
        expected_output = "There was an error while serializing the result of get-summary"
        assert expected_output in result.output

    @patch("fortran_cli.SerializerRegistry.get_serializer")
    def test_get_summary_generic_exception(self, mock_registry, runner, live_data_path):
        mock_registry.return_value.serialize_get_summary.side_effect = Exception
        result = runner.invoke(
            cli,
            [
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                "./output.json",
                "get-summary",
            ],
        )
        expected_output = "An unknown error occurred while serializing the result of get-summary."
        assert expected_output in result.output

    def test_list_all_variables(self, configured_runner):
        result = configured_runner.invoke(cli, ["list-all-variables"])
        assert result.exit_code == 0

        expected_messages = [
            "# of files: 9",
            "# of FORTRAN files: 9",
            "# of FORTRAN files that failed parsing: 0",
            "> FORTRAN file",
            "> Number of components in file:",
            "> Components in file:",
            "VARIABLES",
            "SUBPROGRAMS",
        ]
        for message in expected_messages:
            assert message in result.output

    @patch("fortran_cli.SerializerRegistry.get_serializer")
    def test_list_all_variables_file_not_found_error(self, mock_registry, runner, live_data_path):
        mock_registry.return_value.serialize_list_all_variables.side_effect = FileNotFoundError
        result = runner.invoke(
            cli,
            [
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                "./output.json",
                "list-all-variables",
            ],
        )
        expected_output = "There was an error while serializing the result of list-all-variables"
        assert expected_output in result.output

    @patch("fortran_cli.SerializerRegistry.get_serializer")
    def test_list_all_variables_generic_exception(self, mock_registry, runner, live_data_path):
        mock_registry.return_value.serialize_list_all_variables.side_effect = Exception
        result = runner.invoke(
            cli,
            [
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                "./output.json",
                "list-all-variables",
            ],
        )
        expected_output = "An unknown error occurred while serializing the result of list-all-variables."
        assert expected_output in result.output
