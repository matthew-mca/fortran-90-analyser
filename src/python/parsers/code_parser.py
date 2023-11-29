from typing import List

from code_data_models.code_block import CodeBlock
from code_data_models.code_line import CodeLine
from code_data_models.code_pattern import CodePattern
from code_data_models.fortran_module import FortranModule
from code_data_models.fortran_program import FortranProgram
from code_data_models.fortran_type import FortranType


class CodeParser:
    def build_code_block_object(self, block_type: str, contents: List[CodeLine]) -> CodeBlock:
        if block_type == CodePattern.MODULE:
            return self._build_module(contents)
        if block_type == CodePattern.PROGRAM:
            return self._build_program(contents)
        if block_type == CodePattern.TYPE:
            return self._build_type(contents)

    # These functions shall soon house extra logic,
    # but for now they just instantiate an object and send it back.
    def _build_module(self, contents: List[CodeLine]) -> FortranModule:
        return FortranModule(contents)

    def _build_program(self, contents: List[CodeLine]) -> FortranProgram:
        return FortranProgram(contents)

    def _build_type(self, contents: List[CodeLine]) -> FortranType:
        return FortranType(contents)
