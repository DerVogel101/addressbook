class ContextSupport:
    """
    A context manager class that wraps an object and delegates the context management methods
    (__enter__ and __exit__) to the wrapped object if they exist.

    Attributes:
    -----------
    wrapped : object
        The object to be wrapped by the context manager.

    Methods:
    --------
    __enter__() -> object:
        Enters the runtime context and returns the wrapped object.
        If the wrapped object has an __enter__ method, it is called.

    __exit__(exc_type, exc_val, exc_tb) -> None:
        Exits the runtime context.
        If the wrapped object has an __exit__ method, it is called with the exception details.
    """

    def __init__(self, wrapped):
        """
        Initializes the ContextSupport with the object to be wrapped.

        Parameters:
        -----------
        wrapped : object
            The object to be wrapped by the context manager.
        """
        self.wrapped = wrapped

    def __enter__(self):
        """
        Enters the runtime context and returns the wrapped object.
        If the wrapped object has an __enter__ method, it is called.

        Returns:
        --------
        object
            The wrapped object.
        """
        if hasattr(self.wrapped, "__enter__"):
            self.wrapped.__enter__()
        return self.wrapped

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime context.
        If the wrapped object has an __exit__ method, it is called with the exception details.

        Parameters:
        -----------
        exc_type : type
            The exception type.
        exc_val : Exception
            The exception value.
        exc_tb : traceback
            The traceback object.
        """
        if hasattr(self.wrapped, "__exit__"):
            self.wrapped.__exit__(exc_type, exc_val, exc_tb)