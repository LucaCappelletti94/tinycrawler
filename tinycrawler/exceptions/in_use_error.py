class InUseError(RuntimeError):
    def __init__(self):
        super(InUseError, self).__init__(
            "Object cannot be used as it is already in use.")
