class UnavailableError(RuntimeError):
    def __init__(self):
        super(UnavailableError, self).__init__(
            "Object is not available yet, check for availability using the is_available method before calling use.")
