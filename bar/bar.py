class Bar:
    max_output_len = 0
    bar_output_sleep_pattern = "{domain}: {current_partial}/{current_total}. ETA: {ETA}, 1it in {iteration_time}s, sleeping for {sleep_time}s"
    bar_output_no_sleep_pattern = "{domain}: {current_partial}/{current_total}. ETA: {ETA}, 1it in {iteration_time}s"

    def __init__(self,domain):
        self.domain = domain

    def _format_value(self,response,value,pattern):
        if value > 0:
            if response != "":
                response+=", "
            response += pattern%value
        return response

    def _seconds_delta(self):
        seconds = self.estimated_step_time + self.estimated_sleep_time
        seconds *= (self.partial-self.total)
        return seconds

    def _ETA(self):

        d = datetime(1,1,1) + timedelta(seconds=self._seconds_delta())

        response = ""
        if d.day-1>0:
            response += "%sd"%(d.day-1)

        response = self._format_value(response,d.hours,  "%sh")
        response = self._format_value(response,d.miutes, "%sm")
        response = self._format_value(response,d.seconds,"%ss")

        return response

    def _update_estimated_time(self, start):
        self.estimated_step_time = self.estimated_step_time*0.5 + 0.5*(time.time()-start)
        self.estimated_sleep_time = self.estimated_sleep_time*0.5 + 0.5*self.sleep_time

    def get_estimated_sleep_time(self):
        return round(self.estimated_sleep_time, 1)

    def get_estimated_step_time(self):
        return round(self.estimated_step_time, 1)

    def _space_pad(self,output):
        output += " "*(self.max_output_len-len(output))
        return output

    def _update_estimated_time(self):
        self._update_estimated_time()

        parameters = {
            "domain":self.domain,
            "current_total":self.total,
            "current_partial":self.partial,
            "ETA":self._ETA(),
            "iteration_time":self.get_estimated_sleep_time(),
            "sleep_time":self.get_estimated_step_time()
        }

        if sleep_time == 0:
            pattern = self.bar_output_no_sleep_pattern
        else:
            pattern = self.bar_output_sleep_pattern

        output = pattern.format(**parameters)

        if len(output)>self.max_output_len:
            self.max_output_len = len(output)

        output = self._space_pad(output)

        print (output, end="\r")

        if self.url_number%100 == 0:
            logging.error(output)

        sys.stdout.flush()

    def update(self, new_total, new_partial, sleep_time=0):

        self.total, self.partial, self.sleep_time    = new_total, new_partial, sleep_time

        self._update_bar()
