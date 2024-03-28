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
    "files": [
        {
            "filePath": string,
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
| fileCount | int | The number of FORTRAN files found during parsing. |
| files | list | The FORTRAN files found during parsing. |
| filePath | string | The path to the file from the root of the codebase.  If a single file was specified for parsing, this value is the absolute path of the file. |
| contents | list | A list of all the lines of text in the file. |

## get-summary

### Response Structure

```json
{
    "fileCount": int,
    "commentCount": int,
    "functionCount": int,
    "interfaceCount": int,
    "moduleCount": int,
    "programCount": int,
    "subroutineCount": int,
    "typeCount": int
}
```

### Response Fields

| Property Name | Value | Description |
|---|---|---|
| fileCount | int | The number of FORTRAN files found during parsing. |
| commentCount | int | The number of code comments found. |
| functionCount | int | The number of functions found. |
| interfaceCount | int | The number of interfaces found. |
| moduleCount | int | The number of modules found. |
| programCount | int | The number of programs found. |
| subroutineCount | int | The number of subroutines found. |
| typeCount | int | The number of derived type declarations found. |

## list-all-variables

### Response Structure

```json
{
    "fileCount": int,
    "noDuplicateVariableInformation": boolean,
    "files": [
        {
            "filePath": string,
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
| fileCount | int | The number of FORTRAN files found during parsing. |
| noDuplicateVariableInformation | boolean | Stops variables found in the subprograms for a larger program unit from appearing more than once in the output. |
| files | list | The FORTRAN files found during parsing. |
| filePath | string | The path to the file from the root of the codebase. If a single file was specified for parsing, this value is the absolute path of the file. |
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
