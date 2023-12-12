class DigitalFile:
    """A digital computer file.

    Attributes:
        file_name: The name of the file.
    """

    def __init__(self, file_name: str) -> None:
        """Initialises a file object.

        Args:
            file_name: The name to give the file.
        """

        self.file_name: str = file_name
