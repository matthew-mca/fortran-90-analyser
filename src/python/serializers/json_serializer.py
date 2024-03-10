import json
from typing import Any, Dict

from code_data_models.code_block import CodeBlock
from code_data_models.fortran_function import FortranFunction
from code_data_models.fortran_interface import FortranInterface
from code_data_models.fortran_module import FortranModule
from code_data_models.fortran_program import FortranProgram
from code_data_models.fortran_subroutine import FortranSubroutine
from code_data_models.fortran_type import FortranType
from code_data_models.variable import Variable

from .serializers import Serializer, SerializerRegistry


@SerializerRegistry.register("json")
class _JSONSerializer(Serializer):
    """A serializer class for the JSON format.

    For more information, please see the 'Serializer' base class in the
    'serializers.py' file. Information for any functions not documented
    in this class are available there.
    """

    def _write_json_to_file(self, json_output: Dict[str, Any]) -> None:
        """Writes the results of a class function to a JSON file.

        Args:
            json_output: The dictionary to be output as a JSON object.

        Raise:
            FileNotFoundError: The output path for the serializer is not
              valid.
        """

        with open(self.output_path, "w") as f:
            json.dump(json_output, f, indent=4)

    def serialize_get_raw_contents(self) -> None:
        output: Dict[str, Any] = {}

        output["fileCount"] = len(self.fortran_files)
        output["files"] = []
        for f90_file in self.fortran_files:
            output["files"].append(
                {"filePath": f90_file.path_from_root, "contents": [line.content for line in f90_file.contents]}
            )

        self._write_json_to_file(output)

    def serialize_get_summary(self) -> None:
        output: Dict[str, Any] = {}

        output["fileCount"] = len(self.fortran_files)
        output["commentCount"] = 0
        output["functionCount"] = 0
        output["interfaceCount"] = 0
        output["moduleCount"] = 0
        output["programCount"] = 0
        output["subroutineCount"] = 0
        output["typeCount"] = 0

        for f90_file in self.fortran_files:
            output["commentCount"] += len([line for line in f90_file.contents if line.contains_comment])

            for component in f90_file.components:
                if isinstance(component, FortranFunction):
                    output["functionCount"] += 1
                elif isinstance(component, FortranInterface):
                    output["interfaceCount"] += 1
                elif isinstance(component, FortranModule):
                    output["moduleCount"] += 1
                elif isinstance(component, FortranProgram):
                    output["programCount"] += 1
                elif isinstance(component, FortranSubroutine):
                    output["subroutineCount"] += 1
                elif isinstance(component, FortranType):
                    output["typeCount"] += 1

        self._write_json_to_file(output)

    def serialize_list_all_variables(self) -> None:
        def build_component_json(component: CodeBlock) -> Dict[str, Any]:
            class_name = type(component).__name__
            component_json: Dict[str, Any] = {
                "blockType": class_name.replace("Fortran", "").lower(),
            }

            if hasattr(component, "block_name"):
                component_json["blockName"] = component.block_name

            if hasattr(component, "variables"):
                component_json["variables"] = [build_variable_json(var) for var in component.variables]

            return component_json

        def build_variable_json(variable: Variable) -> Dict[str, Any]:
            return {
                "variableName": variable.name,
                "dataType": variable.data_type,
                "attributes": variable.attributes,
                "lineDeclared": variable.line_declared,
                "possiblyUnused": variable.possibly_unused,
                "isArray": variable.is_array,
                "isPointer": variable.is_pointer,
            }

        output: Dict[str, Any] = {}

        output["fileCount"] = len(self.fortran_files)
        output["files"] = []

        for f90_file in self.fortran_files:
            output["files"].append(
                {
                    "filePath": f90_file.path_from_root,
                    "components": [build_component_json(component) for component in f90_file.components],
                }
            )

        self._write_json_to_file(output)
