from datetime import datetime, timedelta


class Time:
    def __init__(self):
        pass

    def _format_value(self, response, value, pattern):
        if value > 0:
            if response != "":
                response += ", "
            response += pattern.format(value=value)
        return response

    def seconds_to_string(self, delta):
        if delta <= 1:
            return "now"

        d = datetime(1, 1, 1) + timedelta(seconds=delta)

        eta = ""
        if d.day - 1 > 0:
            eta += "%sd" % (d.day - 1)

        eta = self._format_value(eta, d.hour,  "{value}h")
        eta = self._format_value(eta, d.minute, "{value}m")
        eta = self._format_value(eta, d.second, "{value}s")

        return eta
