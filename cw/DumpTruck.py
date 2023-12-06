from queue import PriorityQueue
from random import random
from Element import Element
from FunRand import FunRand


class DumpTruck(Element):
    def __init__(self, delay, workerCount, prepareDelay, id):
        super().__init__(delay, workerCount, id)
        self.maxqueue = float('inf')
        self.meanQueue = 0.0
        self.waitStart = 0.0
        self.stateSum = 0.0
        self.waitTime = 0.0
        self.swapCount = 0
        self.failure = 0
        self.parallelLoader = None
        self.prepareDelayDev = 0
        self.prepareDelayDistribution = ''
        self.prepareDelayMean = prepareDelay
        super().putTnext((float('inf'), 'work'))

    def inAct(self):
        super().putTnext((super().getTcurr() + self.getDelay(), 'work'))
        if super().getState() == 0:
            self.waitTime += super().getTcurr() - self.waitStart

    def outAct(self):
        prevState = super().getTnext(full=True)[1]
        if prevState == 'prepare':
            super().setState(super().getState() - 1)
            self.waitStart = super().getTcurr()
        elif prevState == 'work':
            super().outAct()
            super().putTnext((super().getTcurr() + self.getPrepareDelay(), 'prepare'))
            super().getNextElement().inAct()

        super().popTnextQueue()

    def getFailure(self):
        return self.failure

    def getMaxqueue(self):
        return self.maxqueue

    def setMaxqueue(self, maxqueue):
        self.maxqueue = maxqueue

    def printInfo(self):
        super().printInfo()
        print("failure: " + str(self.getFailure()))

    def doStatistics(self, delta):
        self.stateSum += delta * super().getState()
        self.meanQueue = self.getMeanQueue() + super().getQueue() * delta

    def getMeanQueue(self):
        return self.meanQueue

    def setPrepareDev(self, dev):
        self.prepareDelayDev = dev

    def getPrepareDev(self):
        return self.prepareDelayDev

    def getPrepareDelayDistribution(self):
        return self.prepareDelayDistribution

    def setPrepareDelayDistribution(self, dist):
        self.prepareDelayDistribution = dist

    def getPrepareDelayMean(self):
        return self.prepareDelayMean

    def setPrepareDelayMean(self, mean):
        self.prepareDelayMean = mean

    def getDelay(self):
        delays = self.getDelayMean()
        dists = self.getDistribution()
        devs = self.getDelayDev()
        sum = 0
        for i in range(len(delays)):
            if dists[i].lower() == "exp":
                delay = FunRand.Exp(delays[i])
            elif dists[i].lower() == "norm":
                delay = FunRand.Norm(delays[i], devs[i])
            elif dists[i].lower() == "unif":
                delay = FunRand.Unif(delays[i], devs[i])
            elif dists[i].lower() == "erlang":
                delay = FunRand.Erlang(delays[i], devs[i])
            else:
                delay = self.getDelayMean()
            sum += delay
        return sum

    def getPrepareDelay(self):
        if self.getPrepareDelayDistribution().lower() == "exp":
            delay = FunRand.Exp(self.getPrepareDelayMean())
        elif self.getPrepareDelayDistribution().lower() == "norm":
            delay = FunRand.Norm(self.getPrepareDelayMean(), self.getPrepareDev())
        elif self.getPrepareDelayDistribution().lower() == "unif":
            delay = FunRand.Unif(self.getPrepareDelayMean(), self.getPrepareDev())
        elif self.getPrepareDelayDistribution().lower() == "erlang":
            delay = FunRand.Erlang(self.getPrepareDelayMean(), self.getPrepareDev())
        else:
            delay = self.getPrepareDelayMean()

        return delay
