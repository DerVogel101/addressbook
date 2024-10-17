class ContextSupport:
    """
    A context manager class that wraps an object and delegates the context management methods
    (__enter__ and __exit__) to the wrapped object if they exist.

    :param wrapped: The object to be wrapped by the context manager.
    :type wrapped: object
    :ivar wrapped: The object to be wrapped by the context manager.
    :vartype wrapped: object
    """

    def __init__(self, wrapped):
        """
        Initializes the ContextSupport with the object to be wrapped.

        :param wrapped: The object to be wrapped by the context manager.
        :type wrapped: object
        """
        self.wrapped = wrapped

    def __enter__(self) :
        """
        Enters the runtime context and returns the wrapped object.
        If the wrapped object has an __enter__ method, it is called.

        :return: The wrapped object.
        :rtype: object
        """
        if hasattr(self.wrapped, "__enter__"):
            self.wrapped.__enter__()
        return self.wrapped

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime context.
        If the wrapped object has an __exit__ method, it is called with the exception details.

        :param exc_type: The exception type.
        :type exc_type: type
        :param exc_val: The exception value.
        :type exc_val: Exception
        :param exc_tb: The traceback object.
        :type exc_tb: Traceback
        """
        if hasattr(self.wrapped, "__exit__"):
            self.wrapped.__exit__(exc_type, exc_val, exc_tb)