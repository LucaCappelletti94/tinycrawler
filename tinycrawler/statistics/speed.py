from time import time


class Speed:
    INTERVAL = 1 * 60

    def __init__(self, unit):
        self._unit = unit
        self._total = []
        self._start = time()

    def update(self, value):
        self._total.append({
            "value": value,
            "timestamp": time()
        })

    def _format_speed(self):
        speed = self.get_speed()
        for u in ['', 'K', 'M', 'G']:
            if speed < 1024:
                break
            speed /= 1024

        if abs(speed) > 1:
            unit_pattern = "{unit}/{seconds}"
            speed_format = round(speed, 2)
        else:
            unit_pattern = "{seconds}/{unit}"
            if speed == 0:
                speed_format = "infinite"
            else:
                speed_format = round(1/speed, 2)

        unit = unit_pattern.format(seconds="s", unit=self._unit)

        return "{speed}{u} {unit}".format(speed=speed_format, u=u, unit=unit)

    def get_speed(self):
        now = time()
        current = now - self.INTERVAL
        delta = min(self.INTERVAL, now - self._start)
        total = 0
        for i, info in reversed(list(enumerate(self._total))):
            if info["timestamp"] < current:
                break
            total += info["value"]
        self._total = self._total[i:]

        return total / delta

    def get_formatted_speed(self):
        return self._format_speed()
