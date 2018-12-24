class MaxFileSize(RuntimeError):
    def __init__(self):
        super(MaxFileSize, self).__init__(
            "File is bigger than allowed.")
