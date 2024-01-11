from typing import Any


def build_repr_from_object(target_object: Any) -> str:
    """Builds a string representation of an object that includes all of its attributes.

    Args:
        target_object: The object to look at when building the string.
    """

    class_name = type(target_object).__name__

    return build_repr_from_attributes(class_name, **vars(target_object))


def build_repr_from_attributes(class_name: str, **kwargs: Any) -> str:
    """Builds a string from a provided class name and list of attributes.

    Args:
        class_name: The name of the class that will use the string.
        **kwargs: The names and values of the attributes to include in the string.
    """

    attributes = []
    for attribute, attr_value in kwargs.items():
        attributes.append(f"{attribute}={attr_value!r}")

    attribute_string = ", ".join(attributes)

    return f"{class_name}({attribute_string})"
