class UnavailableError(RuntimeError):
    def __init__(self):
        super(UnavailableError, self).__init__(
            "Object is not available yet.")
