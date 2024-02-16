from typing import Any


def build_repr_from_object(target_object: Any) -> str:
    """Builds a repr using all the attributes of the provided object.

    Args:
        target_object: The object to look at when building the string.

    Returns:
        A string repr of the object that contains all of the object's
        attributes.
    """

    return build_repr_from_attributes(target_object, **vars(target_object))


def build_repr_from_attributes(target_object: Any, **kwargs: Any) -> str:
    """Builds a string from a provided object and a list of attributes.

    Builds a repr for a provided object. The object is parsed to work
    out its class name, and any key-word arguments provided are listed
    as part of the repr. This allows a developer to manually provide
    the fields that should be included as part of the repr string.

    Args:
        class_name: The name of the class that will use the string.
        **kwargs: The names and values of the attributes to include in
          the string.

    Returns:
        A string repr of the object that contains the provided
        key-word arguments.
    """

    class_name = type(target_object).__name__

    attributes = []
    for attribute, attr_value in kwargs.items():
        attributes.append(f"{attribute}={attr_value!r}")

    attribute_string = ", ".join(attributes)

    return f"{class_name}({attribute_string})"
