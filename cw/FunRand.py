import random
import math


class FunRand:

    @staticmethod
    def Exp(timeMean):
        a = 0
        while a == 0:
            a = random.random()
        a = -timeMean * math.log(a)
        return a if a > 0 else 0.1

    @staticmethod
    def Unif(timeMin, timeMax):
        a = 0
        while a == 0:
            a = random.random()
        a = timeMin + a * (timeMax - timeMin)
        return a if a > 0 else 0.1

    @staticmethod
    def Norm(timeMean, timeDeviation):
        r = random.Random()
        a = r.gauss(timeMean, timeDeviation)
        return a if a > 0 else 0.1

    @staticmethod
    def Erlang(timeMean, k):
        sum = 0
        for i in range(k):
            a = 0
            while a == 0:
                a = random.random()
            a = -timeMean * math.log(a)
            sum += a
        return sum if sum > 0 else 0.1




