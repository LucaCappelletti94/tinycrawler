from time import time


class Speed:
    SECONDS = "s"

    def __init__(self, unit):
        self._unit = unit
        self._total = 0
        self._start = time()

    def update(self, value):
        self._total += value

    def _format_speed(self):
        speed = self.get_speed()
        for u in ['', 'K', 'M', 'G']:
            if speed < 1024:
                break
            speed /= 1024

        if abs(speed) > 1:
            unit = "%s/%s" % (self._unit, self.SECONDS)
        else:
            unit = "%s/%s" % (self.SECONDS, self._unit)
            speed = 1 / speed

        return "%s%s %s" % (round(speed, 2), u, unit)

    def get_speed(self):
        delta = time() - self._start
        return self._total / delta

    def get_formatted_speed(self):
        return self._format_speed()
