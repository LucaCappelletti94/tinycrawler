class Queue:
    def add(self, element, **kwargs):
        raise NotImplementedError(
            "Method `add` has to be implemented in subclasses of Queue."
        )

    def pop(self, **kwargs):
        raise NotImplementedError(
            "Method `pop` has to be implemented in subclasses of Queue."
        )
