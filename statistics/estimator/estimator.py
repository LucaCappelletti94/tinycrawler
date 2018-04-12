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
        s = self._growth.position() - self._decline.position()
        v = self._growth.speed() - self._decline.speed()
        a = self._growth.acceleration() - self._decline.acceleration()
        #j = self._growth.jerk() - self._decline.jerk()

        if a>=0:
            return None

        return self._roots(s,v,a)

    # def _roots(self,a,b,c,d):
    #     d2 = d*d
    #     v3d = 3*d
    #     c2 = c*c
    #     c3 = c2*c
    #     v9bcd = 3*b*c*v3d
    #     r32 = 2**(1/3)
    #     first_term = (-27*a*d2+v9bcd-2*c3)**2

    #     second_term = v3d*b-c2
    #     delta = first_term + 4*(second_term**3)

    #     if delta < 0:
    #         return None

    #     root = math.sqrt(delta)

    #     root3 = self.cuberoot(root - 27*a*d2+v9bcd-2*c3)

    #     first = root3/(v3d*r32)

    #     second = r32*(v3d*b-c2)/(v3d*root3)

    #     third = c/(v3d)

    #     return first - second - third

    def _root(self, a, b, c):
        delta = b*b - 4*a*c
        if delta < 0:
            return None

        return (-b + delta) / (2*c)

    def cuberoot(self, z):
        return np.sign(z)*abs(z)**(1/3)

    def get_growth_speed(self):
        return self._growth.speed()

    def get_decline_speed(self):
        return self._decline.speed()