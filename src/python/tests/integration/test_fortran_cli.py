import pytest
from click.testing import CliRunner

from fortran_cli import cli


class TestFortranCLI:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def live_data_path(self):
        return "./src/python/tests/integration/.live_test_data"

    def test_get_summary(self, runner, live_data_path):
        result = runner.invoke(cli, ["get-summary", "--code-path", live_data_path])
        summary_output = result.output.split("\n")

        expected_metrics = {
            "Fortran 90 files": 9,
            "Functions": 8,
            "Interfaces": 0,
            "Modules": 0,
            "Programs": 9,
            "Subroutines": 2,
            "Derived Types": 0,
        }

        for unit_type, expected_count in expected_metrics.items():
            assert f"# of {unit_type}: {expected_count}" in summary_output

    # TODO: Find more Fortran 90 test data that is available for use in these live tests
