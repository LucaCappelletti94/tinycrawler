from .derivative import derivative
import math
import numpy as np


class time_estimator:
    def __init__(self):
        self._growth = derivative(2)
        self._decline = derivative(2)

    def step_decline(self, decline_new_position):
        self._decline.step(decline_new_position)

    def step_growth(self, growth_new_position):
        self._growth.step(growth_new_position)

    def get_time_estimate(self):
        if self._decline.speed()==0:
            return None

        return (self._growth.position() - self._decline.position())/self._decline.speed()

    def get_growth_speed(self):
        return self._growth.speed()

    def get_decline_speed(self):
        return self._decline.speed()