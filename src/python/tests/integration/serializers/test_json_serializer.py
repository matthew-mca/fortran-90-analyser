import json

import pytest
from click.testing import CliRunner

from fortran_cli import cli


class TestJSONSerializer:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def live_data_path(self):
        return "./src/python/tests/integration/.live_test_data/Fortran"

    def test_get_raw_contents(self, runner, live_data_path, tmp_path):
        output_path = tmp_path / "grc.json"
        result = runner.invoke(
            cli,
            [
                "--fortran-only",
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                output_path,
                "get-raw-contents",
            ],
        )

        assert result.exit_code == 0
        assert "Results serialized successfully" in result.output

        with open(output_path, "r") as f:
            data = json.load(f)

        assert data["fileCount"] == len(data["files"])

        for file_dict in data["files"]:
            assert file_dict["filePath"].endswith(".f90")
            assert isinstance(file_dict["contents"], list)

    def test_get_summary(self, runner, live_data_path, tmp_path):
        output_path = tmp_path / "gs.json"
        result = runner.invoke(
            cli,
            [
                "--fortran-only",
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                output_path,
                "get-summary",
                "--top-level-blocks",
            ],
        )

        assert result.exit_code == 0
        assert "Results serialized successfully" in result.output

        with open(output_path, "r") as f:
            data = json.load(f)

        assert data["fileCount"] == 9
        assert data["commentCount"] == 108
        assert data["topLevelCodeBlocksOnly"] is True
        assert data["topLevelVariablesOnly"] is False

        code_block_dict = data["codeBlockTypeSummary"]
        assert isinstance(code_block_dict, dict)
        assert len(code_block_dict) == 8
        assert all(isinstance(value, int) for value in code_block_dict.values())

        variable_dict = data["variableDataTypeSummary"]
        assert isinstance(variable_dict, dict)
        assert len(variable_dict) == 7
        assert all(isinstance(value, int) for value in variable_dict.values())

    def test_list_all_variables(self, runner, live_data_path, tmp_path):
        output_path = tmp_path / "lav.json"
        result = runner.invoke(
            cli,
            [
                "--fortran-only",
                "--code-path",
                live_data_path,
                "--output-format",
                "json",
                "--output-path",
                output_path,
                "list-all-variables",
                "--no-duplicates",
            ],
        )

        assert result.exit_code == 0
        assert "Results serialized successfully" in result.output

        with open(output_path, "r") as f:
            data = json.load(f)

        assert data["fileCount"] == len(data["files"])
        assert data["noDuplicateVariableInformation"] is True

        for file_dict in data["files"]:
            assert file_dict["filePath"].endswith(".f90")
            assert file_dict["componentCount"] == len(file_dict["components"])

            for component in file_dict["components"]:
                assert "blockType" in component.keys()
                assert "startLineNumber" in component.keys()
                assert "endLineNumber" in component.keys()
                if component["blockType"] in ("function, subroutine"):
                    assert "isRecursive" in component.keys()
