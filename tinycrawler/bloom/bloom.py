from pybloom_live import BloomFilter


class Bloom:
    def __init__(self, n=3, capacity=1e9):
        self._filters = [
            BloomFilter(
                capacity=capacity,
                error_rate=0.1 ** (i + 1)
            ) for i in range(n)
        ]

    def put(self, value):
        """Add given value to all filters."""
        [bf.add(value) for bf in self._filters]

    def __contains__(self, value):
        """Return boolean representing if given value is present in all filters."""
        return all([value in bf for bf in self._filters])
