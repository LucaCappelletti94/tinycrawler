from datetime import datetime, timedelta


class Time:

    def get_remaining_time(growing_speed, shrinking_speed, total):
        speed_delta = shrinking_speed - growing_speed

        if total <= 10:
            return "now"
        if speed_delta <= 0:
            return "infinite"

        return Time.seconds_to_string(total / growing_speed)

    def _format_value(response, value, pattern):
        if value > 0:
            if response != "":
                response += ", "
            response += pattern % value
        return response

    def seconds_to_string(delta):
        if delta <= 1:
            return "now"

        d = datetime(1, 1, 1) + timedelta(seconds=delta)

        eta = ""
        if d.day - 1 > 0:
            eta += "%sd" % (d.day - 1)

        eta = Time._format_value(eta, d.hour,  "%sh")
        eta = Time._format_value(eta, d.minute, "%sm")
        eta = Time._format_value(eta, d.second, "%ss")

        return eta
