

import sys
import time
from datetime import datetime, timedelta

class Bar:
    max_output_len = 0
    bar_output_pattern = "{domain}: {current_partial}/{current_total}. ETA: {ETA}, {iterations} it / {seconds} s"
    estimated_step_time = 0

    def __init__(self,domain):
        self.domain = domain
        self.start = time.time()

    def _format_value(self,response,value,pattern):
        if value > 0:
            if response != "":
                response+=", "
            response += pattern%value
        return response

    def _seconds_delta(self):
        return self.estimated_step_time*(self.total-self.partial)

    def _ETA(self):

        d = datetime(1,1,1) + timedelta(seconds=self._seconds_delta())

        response = ""
        if d.day-1>0:
            response += "%sd"%(d.day-1)

        response = self._format_value(response,d.hour,  "%sh")
        response = self._format_value(response,d.minute, "%sm")
        response = self._format_value(response,d.second,"%ss")

        return response

    def _update_estimated_time(self):
        if self.estimated_step_time == 0:
            self.estimated_step_time = time.time()-self.start
        else:
            self.estimated_step_time = self.estimated_step_time*0.995 + 0.005*(time.time()-self.start)

    def _space_pad(self,output):
        output += " "*(self.max_output_len-len(output))
        return output

    def _update_bar(self):
        self._update_estimated_time()

        seconds = self.estimated_step_time

        if seconds<1 and seconds != 0:
            iterations = round(1/seconds, 2)
            seconds = 1
        else:
            iterations = 1
            seconds = round(self.estimated_step_time, 2)

        parameters = {
            "domain":self.domain,
            "current_total":self.total,
            "current_partial":self.partial,
            "ETA":self._ETA(),
            "iterations": iterations,
            "seconds": seconds
        }

        output = self.bar_output_pattern.format(**parameters)

        if len(output)>self.max_output_len:
            self.max_output_len = len(output)

        output = self._space_pad(output)

        print (output, end="\r")

        sys.stdout.flush()
        self.start = time.time()

    def update(self, new_total, new_partial):
        self.total, self.partial = new_total, new_partial
        self._update_bar()
