import pytest

from code_data_models.code_pattern import CodePattern
from code_data_models.fortran_module import FortranModule
from code_data_models.fortran_program import FortranProgram
from code_data_models.fortran_type import FortranType
from parsers.code_parser import CodeParser


class TestCodeParser:
    @pytest.mark.parametrize(
        "block_type,contents,result_type",
        [
            (CodePattern.MODULE, [], FortranModule),
            (CodePattern.PROGRAM, [], FortranProgram),
            (CodePattern.TYPE, [], FortranType),
        ],
    )
    def test_build_code_block_object(self, block_type, contents, result_type):
        parser = CodeParser()
        result = parser.build_code_block_object(block_type, contents)
        assert isinstance(result, result_type)
