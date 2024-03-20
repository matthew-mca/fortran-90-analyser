import os
from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Union

from file_data_models.fortran_file import FortranFile


class Serializer(ABC):
    """A serializer for the commands available in fortran_cli.py.

    An abstract serializer base class that defines the serialization
    functions that a child class must implement. These functions must be
    implemented in order for a child class to be considered a functional
    serializer available for use in the application's CLI. Every unique
    command in the analyser has its own 'serialize' function.

    Attributes:
        output_path: The path the serializer writes to when called.
        fortran_files: The file(s) collected by the application's file
          parser. These files are then processed during serialization.
    """

    def __init__(self, output_path: str, fortran_files: List[FortranFile]):
        """Initialises a Serializer object.

        This __init__ can only be called by fully implemented child
        classes that inherit from Serializer.

        Args:
            output_path: The path the serializer writes to when called.
            fortran_files: The file(s) collected by the application's
              file parser. These files are then processed during
              serialization.
        """

        self.output_path = os.path.abspath(output_path)
        self.fortran_files = fortran_files

    @abstractmethod
    def serialize_get_raw_contents(self) -> None:
        """Serializes the results of the get-raw-contents command."""
        pass

    @abstractmethod
    def serialize_get_summary(self) -> None:
        """Serializes the results of the get-summary command."""
        pass

    @abstractmethod
    def serialize_list_all_variables(self, no_duplicates: bool) -> None:
        """Serializes the results of the list-all-variables command.

        Args:
            no_duplicates: Stops variables found in the subprograms for
              a larger program unit from appearing more than once.
              Variables inside of any subprograms are only listed as
              part of the subprogram's variables, and not as part of the
              larger program unit's variables.
        """
        pass


class SerializerRegistry:
    """A registry for storing and obtaining Serializer child classes.

    This class stores all of the fully implemented serializers in the
    application. There is a function available for registering
    serializers, as well as a function for obtaining the correct type
    of serializer using a provided key. Any use of serializers in the
    project should retrieve them through this registry.

    Attributes:
        _serializers: An internal dict that contains all the serializer
          classes that are registered into the Serializer Registry.
    """

    _serializers: Dict[str, Serializer] = {}

    @classmethod
    def register(cls, format: str) -> Callable:
        """A decorator for registering new serializers.

        Once a new serializer class is implemented, this decorator can
        be added to the top of the class declaration. As long as the
        class is decorated with this decorator and there is an import
        statement for the decorated class in the __init__ file at the
        root of the 'serializers' package, it will appear in the
        Serializer Registry.

        Args:
            format: The format the Serializer child class is responsible
              for serializing to. The key given to each decorated class
              must be unique!
        """

        def wrapper(wrapped_cls: Serializer) -> Serializer:
            cls._serializers[format] = wrapped_cls
            return wrapped_cls

        return wrapper

    @classmethod
    def get_serializer(
        cls, format: str, output_path: str, fortran_files: Union[FortranFile, List[FortranFile]]
    ) -> Serializer:
        """Finds and returns an instance of a serializer.

        Checks the Serializer Registry for a serializer class registered
        with the provided key, and returns an instance of the class if
        one is found. If there is no serializer class registered under
        the provided key, a KeyError is raised.

        Args:
            format: The key of the registered serializer class.
            output_path: The path the serializer writes to when called.
            fortran_files: The file(s) collected by the application's
              file parser. These files are then processed during
              serialization.

        Returns:
            An instance of the class registered under the provided key
            (if a class is found).

        Raises:
            KeyError: There is no serializer in the Serializer Registry
              that is registered under the provided key.
        """

        serializer = cls._serializers[format]
        return serializer(output_path, fortran_files)  # type: ignore[operator]

    @classmethod
    def get_all_serializable_formats(cls) -> List[str]:
        """Returns a list of all the registered serializer formats."""

        return list(cls._serializers.keys())
