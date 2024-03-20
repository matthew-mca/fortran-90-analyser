from typing import Any, Dict

import yaml

from code_data_models.code_block import CodeBlock
from code_data_models.fortran_function import FortranFunction
from code_data_models.fortran_interface import FortranInterface
from code_data_models.fortran_module import FortranModule
from code_data_models.fortran_program import FortranProgram
from code_data_models.fortran_subroutine import FortranSubroutine
from code_data_models.fortran_type import FortranType
from code_data_models.variable import Variable

from .serializers import Serializer, SerializerRegistry


# We override the ignore_aliases function from the yaml Dumper class in
# order to serialize to YAML without generating anchors and aliases.
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data: Any) -> bool:
        return True


@SerializerRegistry.register("yaml")
class _YAMLSerializer(Serializer):
    """A serializer class for the YAML format.

    For more information, please see the 'Serializer' base class in the
    'serializers.py' file. Information for any functions not documented
    in this class are available there.
    """

    def _write_yaml_to_file(self, yaml_output: Dict[str, Any]) -> None:
        """Writes the results of a class function to a YAML file.

        Args:
            yaml_output: The dictionary to be output to a YAML file.

        Raise:
            FileNotFoundError: The output path for the serializer is not
              valid.
        """

        with open(self.output_path, "w") as f:
            yaml.dump(yaml_output, f, Dumper=NoAliasDumper, sort_keys=False)

    def serialize_get_raw_contents(self) -> None:
        output: Dict[str, Any] = {}

        output["fileCount"] = len(self.fortran_files)
        output["files"] = []
        for f90_file in self.fortran_files:
            output["files"].append(
                {"filePath": f90_file.path_from_root, "contents": [line.content for line in f90_file.contents]}
            )

        self._write_yaml_to_file(output)

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

        self._write_yaml_to_file(output)

    def serialize_list_all_variables(self, no_duplicates: bool) -> None:
        def build_component_dict(component: CodeBlock) -> Dict[str, Any]:
            class_name = type(component).__name__
            has_subprograms = hasattr(component, "subprograms")

            component_json: Dict[str, Any] = {
                "blockType": class_name.replace("Fortran", "").lower(),
                "startLineNumber": component.start_line_number,
                "endLineNumber": component.end_line_number,
            }

            if hasattr(component, "block_name"):
                component_json["blockName"] = component.block_name

            if hasattr(component, "is_recursive"):
                component_json["isRecursive"] = component.is_recursive

            if has_subprograms:
                component_json["subprogramCount"] = len(component.subprograms)
                component_json["subprograms"] = [
                    build_component_dict(subprogram) for subprogram in component.subprograms
                ]

            if hasattr(component, "variables"):
                if has_subprograms and no_duplicates:
                    variable_list = component.get_variables_not_in_subprograms()
                else:
                    variable_list = component.variables

                component_json["variableCount"] = len(variable_list)
                component_json["variables"] = [build_variable_dict(var) for var in variable_list]

            return component_json

        def build_variable_dict(variable: Variable) -> Dict[str, Any]:
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
        output["noDuplicateVariableInformation"] = no_duplicates
        output["files"] = []

        for f90_file in self.fortran_files:
            output["files"].append(
                {
                    "filePath": f90_file.path_from_root,
                    "componentCount": len(f90_file.components),
                    "components": [build_component_dict(component) for component in f90_file.components],
                }
            )

        self._write_yaml_to_file(output)
