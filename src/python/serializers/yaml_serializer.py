from collections import defaultdict
from typing import Any, Dict

import yaml

from code_data_models.code_block import CodeBlock
from code_data_models.variable import Variable
from file_data_models.fortran_file import FortranFile

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
        failed_parse_count = sum(item.failed_fortran_parse for item in self.collected_files)

        output["fileCount"] = len(self.collected_files)
        output["fortranFileCount"] = (
            sum(isinstance(item, FortranFile) for item in self.collected_files) + failed_parse_count
        )
        output["fortranFilesFailedToParse"] = failed_parse_count
        output["files"] = []

        for file_obj in self.collected_files:
            file_info = {
                "filePath": file_obj.path_from_root,
                "failedFortranParse": file_obj.failed_fortran_parse,
            }

            if isinstance(file_obj, FortranFile):
                file_info["contents"] = [line.content for line in file_obj.contents]

            output["files"].append(file_info)

        self._write_yaml_to_file(output)

    def serialize_get_summary(self, top_level_blocks: bool, top_level_vars: bool) -> None:
        output: Dict[str, Any] = {}
        failed_parse_count = sum(item.failed_fortran_parse for item in self.collected_files)

        output["fileCount"] = len(self.collected_files)
        output["fortranFileCount"] = (
            sum(isinstance(item, FortranFile) for item in self.collected_files) + failed_parse_count
        )
        output["fortranFilesFailedToParse"] = failed_parse_count
        output["commentCount"] = 0
        found_blocks = []
        found_variables = []

        for file_obj in self.collected_files:
            if not isinstance(file_obj, FortranFile):
                continue

            found_blocks.extend(file_obj.components)
            output["commentCount"] += sum(line.contains_comment for line in file_obj.contents)

        output["topLevelCodeBlocksOnly"] = top_level_blocks
        output["topLevelVariablesOnly"] = top_level_vars

        if not top_level_blocks:
            subprograms = []
            for code_block in found_blocks:
                subprograms.extend(code_block.get_all_subprograms())

            found_blocks.extend(subprograms)

        if not top_level_blocks or top_level_vars:
            for block in found_blocks:
                found_variables.extend(block.get_variables_not_in_subprograms())
        else:
            for block in found_blocks:
                found_variables.extend(block.variables)

        block_counts: Dict[str, int] = defaultdict(int)
        for block in found_blocks:
            class_name = type(block).__name__
            block_counts[class_name] += 1

        variable_counts = {}
        for var_type in Variable.ALL_DATA_TYPES:
            # We do 'in' instead of '==' here since some data types can have
            # extra information as part of the type declaration, e.g
            # 'INTEGER(I8)'.
            variable_counts[var_type] = sum(var_type in var.data_type for var in found_variables)

        output["codeBlockTypeSummary"] = {
            "doLoopCount": block_counts["FortranDoLoop"],
            "functionCount": block_counts["FortranFunction"],
            "ifBlockCount": block_counts["FortranIfBlock"],
            "interfaceCount": block_counts["FortranInterface"],
            "moduleCount": block_counts["FortranModule"],
            "programCount": block_counts["FortranProgram"],
            "subroutineCount": block_counts["FortranSubroutine"],
            "derivedTypeDeclarationCount": block_counts["FortranType"],
        }

        output["variableDataTypeSummary"] = {
            "characterCount": variable_counts["CHARACTER"],
            "complexCount": variable_counts["COMPLEX"],
            "doubleComplexCount": variable_counts["DOUBLE COMPLEX"],
            "doublePrecisionCount": variable_counts["DOUBLE PRECISION"],
            "integerCount": variable_counts["INTEGER"],
            "logicalCount": variable_counts["LOGICAL"],
            "realCount": variable_counts["REAL"],
        }

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
        failed_parse_count = sum(item.failed_fortran_parse for item in self.collected_files)

        output["fileCount"] = len(self.collected_files)
        output["fortranFileCount"] = (
            sum(isinstance(item, FortranFile) for item in self.collected_files) + failed_parse_count
        )
        output["fortranFilesFailedToParse"] = failed_parse_count
        output["noDuplicateVariableInformation"] = no_duplicates
        output["files"] = []

        for file_obj in self.collected_files:
            file_info = {
                "filePath": file_obj.path_from_root,
                "failedFortranParse": file_obj.failed_fortran_parse,
            }

            if isinstance(file_obj, FortranFile):
                file_info["componentCount"] = len(file_obj.components)
                file_info["components"] = [build_component_dict(component) for component in file_obj.components]

            output["files"].append(file_info)

        self._write_yaml_to_file(output)
