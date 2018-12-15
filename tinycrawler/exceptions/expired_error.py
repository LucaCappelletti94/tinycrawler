class ExpiredError(RuntimeError):
    def __init__(self):
        super(ExpiredError, self).__init__(
            "Object has expired. Check the `expired` property for expiration before trying to use object.")
