# Serialiser Output Structure

This document shows examples of the structure of the JSON and YAML serialiser outputs for the
different commands in the application.

***Note:*** *These examples are listed as JSON only. The YAML output, however, includes the same*
*fields as the JSON version, also with the same structure.*

## get-raw-contents

### Response Structure

```json
{
    "fileCount": int,
    "fortranFileCount": int,
    "fortranFilesFailedToParse": int,
    "files": [
        {
            "filePath": string,
            "failedFortranParse": boolean,
            "contents": [
                string
            ]
        }
    ]
}
```

### Response Fields

| Property Name | Value | Description |
|---|---|---|
| fileCount | int | The overall number of files found during parsing. |
| fortranFileCount | int | The number of FORTRAN files found during parsing. |
| fortranFilesFailedToParse | int | The number of FORTRAN files where parsing failed. These files fall back to being minimal file objects. |
| files | list | The FORTRAN files found during parsing. |
| filePath | string | The path to the file from the root of the codebase.  If a single file was specified for parsing, this value is the absolute path of the file. |
| failedFortranParse | boolean | Indicates if this specific file is a FORTRAN file that failed parsing. |
| contents | list | A list of all the lines of text in the file. |

## get-summary

### Response Structure

```json
{
    "fileCount": int,
    "fortranFileCount": int,
    "fortranFilesFailedToParse": int,
    "commentCount": int,
    "topLevelCodeBlocksOnly": boolean,
    "topLevelVariablesOnly": boolean,
    "codeBlockTypeSummary": {
        "doLoopCount": int,
        "functionCount": int,
        "ifBlockCount": int,
        "interfaceCount": int,
        "moduleCount": int,
        "programCount": int,
        "subroutineCount": int,
        "derivedTypeDeclarationCount": int
    },
    "variableDataTypeSummary": {
        "characterCount": int,
        "complexCount": int,
        "doubleComplexCount": int,
        "doublePrecisionCount": int,
        "integerCount": int,
        "logicalCount": int,
        "realCount": int
    }
}
```

### Response Fields

| Property Name | Value | Description |
|---|---|---|
| fileCount | int | The overall number of files found during parsing. |
| fortranFileCount | int | The number of FORTRAN files found during parsing. |
| fortranFilesFailedToParse | int | The number of FORTRAN files where parsing failed. These files fall back to being minimal file objects. |
| commentCount | int | The number of commented lines of code. |
| topLevelCodeBlocksOnly | boolean | Does not include subprogram information in the summary. |
| topLevelVariablesOnly | boolean | Does not include variable information for variables that are found in a program unit's subprograms in the summary. Has no effect if topLevelCodeBlocksOnly is false. |
| codeBlockTypeSummary | dict | A collection of information about the different types of FORTRAN code blocks found during parsing. |
| doLoopCount | int | The number of DO loops. |
| functionCount | int | The number of functions. |
| ifBlockCount | int | The number of IF blocks. |
| interfaceCount | int | The number of interfaces. |
| moduleCount | int | The number of modules. |
| programCount | int | The number of programs. |
| subroutineCount | int | The number of subroutines. |
| derivedTypeDeclarationCount | int | The number of derived type declarations. |
| variableDataTypeSummary | dict | A collection of information about the different variable types found during parsing. |
| characterCount | int | The number of CHARACTER variables. |
| complexCount | int | The number of COMPLEX variables. |
| doubleComplexCount | int | The number of DOUBLE COMPLEX variables. |
| doublePrecisionCount | int | The number of DOUBLE PRECISION variables. |
| integerCount | int | The number of INTEGER variables. |
| logicalCount | int | The number of LOGICAL variables. |
| realCount | int | The number of REAL variables. |

## list-all-variables

### Response Structure

```json
{
    "fileCount": int,
    "fortranFileCount": int,
    "fortranFilesFailedToParse": int,
    "noDuplicateVariableInformation": boolean,
    "files": [
        {
            "filePath": string,
            "failedFortranParse": boolean,
            "componentCount": int,
            "components": [
                type(component)
            ]
        }
    ]
}
```

### Structure of 'component' object

```json
{
    "blockType": string,
    "startLineNumber": int,
    "endLineNumber": int,
    "blockName": string,
    "isRecursive": boolean,
    "subprogramCount": int,
    "subprograms": [
        type(component)
    ],
    "variableCount": int,
    "variables": [
        {
            "variableName": string,
            "dataType": string,
            "attributes": [
                string
            ],
            "lineDeclared": int,
            "possiblyUnused": boolean,
            "isArray": boolean,
            "isPointer": boolean
        }
    ]
}
```

### Response Fields

| Property Name | Value | Description |
|---|---|---|
| fileCount | int | The overall number of files found during parsing. |
| fortranFileCount | int | The number of FORTRAN files found during parsing. |
| fortranFilesFailedToParse | int | The number of FORTRAN files where parsing failed. These files fall back to being minimal file objects. |
| noDuplicateVariableInformation | boolean | Stops variables found in the subprograms for a larger program unit from appearing more than once in the output. |
| files | list | The FORTRAN files found during parsing. |
| filePath | string | The path to the file from the root of the codebase. If a single file was specified for parsing, this value is the absolute path of the file. |
| failedFortranParse | boolean | Indicates if this specific file is a FORTRAN file that failed parsing. |
| componentCount | int | The number of top-level code blocks found in the file. |
| components | list | The top-level code blocks found in the file. |
| blockType | string | The type of the code block, e.g. program, module, function, etc. |
| startLineNumber | int | The number of the line in the file that the code block is declared on. |
| endLineNumber | int | The number of the line in the file that the code block ends on. |
| blockName | string | The name given to the code block (if applicable). |
| isRecursive | boolean | Included for functions and subroutines. Indicates if the function/subroutine is declared as RECURSIVE. |
| subprogramCount | int | The number of code blocks found inside the current code block. |
| subprograms | list | The code blocks found inside the current code block. |
| variableCount | int | The number of variables declared inside the current code block. |
| variables | list | The variables declared inside the current code block. |
| variableName | string | The name of the variable. |
| dataType | string | The variable's data type. |
| attributes | list | The FORTRAN attributes include in the variable declaration. |
| lineDeclared | int | The number of the line in the file that the variable is declared on. |
| possiblyUnused | boolean | Indicates if the analyser has detected that there is a possibility that the variable was declared and then not use afterwards. |
| isArray | boolean | Indicates if the variable is an array. |
| isPointer | boolean | Indicates if the variable is a pointer. |
