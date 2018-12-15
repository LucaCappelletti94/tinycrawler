class NotInUseError(RuntimeError):
    def __init__(self):
        super(NotInUseError, self).__init__(
            "Object cannot be in used state if was not used.")
