class ContextSupport:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __enter__(self):
        if hasattr(self.wrapped, "__enter__"):
            self.wrapped.__enter__()
        return self.wrapped

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self.wrapped, "__exit__"):
            self.wrapped.__exit__(exc_type, exc_val, exc_tb)