class Bar:
      def _estimated_time(self):
        d = datetime(1,1,1) + timedelta(seconds=(self.estimated_step_time+self.estimated_sleep_time)*(len(self.urls)-self.url_number))
        response = ""
        if d.day-1>0:
            response += "%sd"%(d.day-1)

        if d.hour>0:
            if response != "":
                response+=", "
            response += "%sh"%(d.hour)

        if d.minute>0:
            if response != "":
                response+=", "
            response += "%sm"%(d.minute)

        if d.second>0:
            if response != "":
                response+=", "
            response += "%ss"%(d.second)
        return response

    def _update_estimated_time(self, start):
        self.estimated_step_time = self.estimated_step_time*0.5 + 0.5*(time.time()-start)
        self.estimated_sleep_time = self.estimated_sleep_time*0.5 + 0.5*self.sleep_time

    def _update_bar(self):
        output = "%s: %s/%s. ETA: %s, 1it in %ss, sleeping for %ss"%(self._domain, self.url_number, len(self.urls), self._estimated_time(), round(self.estimated_step_time, 1), round(self.estimated_sleep_time, 1))
        if len(output)>self.max_output_len:
            self.max_output_len = len(output)
        output += " "*(self.max_output_len-len(output))
        print (output, end="\r")
        if self.url_number%100 == 0:
            logging.error(output)
        sys.stdout.flush()


    def update(self, new_total, new_partial):
        # To be implemented