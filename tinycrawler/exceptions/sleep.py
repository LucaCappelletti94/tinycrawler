class Sleep(RuntimeError):
    def __init__(self):
        super(Sleep, self).__init__(
            "Assemble or disassembler has nothing more to do and requires to sleep.")
