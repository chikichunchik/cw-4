from queue import PriorityQueue
from random import random
from Element import Element
from FunRand import FunRand

class Loader(Element):
    def __init__(self, delay, workerCount, prepareDelay, id):
        super().__init__(delay, workerCount, id)
        self.maxqueue = float('inf')
        self.meanQueue = 0.0
        self.waitStart = 0.0
        self.stateSum = 0.0
        self.waitTime = 0.0
        self.blocked = 0
        self.passed = 0
        self.failure = 0
        self.blocked_loader = 0
        self.blocked_queue = 0
        self.blocked_dumptruck = 0
        self.parallelLoader = None
        self.prepareDelayDev = 0
        self.prepareDelayDistribution = ''
        self.prepareDelayMean = prepareDelay
        super().putTnext((float('inf'), 'work'))

    def inAct(self):
        queueLoader = self if self.parallelLoader is None else self.parallelLoader
        if super().getState() < super().getWorkerCount() \
                and queueLoader.getQueue() >= 2 \
                and self.getNextElement().getState() < self.getNextElement().getWorkerCount():
            super().setState(super().getState() + 1)
            self.getNextElement().setState(self.getNextElement().getState() + 1)
            super().putTnext((super().getTcurr() + super().getDelay(), 'work'))
            if super().getState() == 0:
                self.waitTime += super().getTcurr() - self.waitStart
            self.passed += 1
        else:
            if queueLoader.getQueue() < self.getMaxqueue():
                queueLoader.setQueue(queueLoader.getQueue() + 1)
            self.blocked += 1
            if not super().getState() < self.getWorkerCount():
                self.blocked_loader += 1
            if not queueLoader.getQueue() >= 2:
                self.blocked_queue += 1
            if not self.getNextElement().getState() < self.getNextElement().getWorkerCount():
                self.blocked_dumptruck += 1

    def outAct(self):
        prevState = super().getTnext(full=True)[1]
        queueLoader = self if self.parallelLoader is None else self.parallelLoader
        if prevState == 'prepare':
            super().setState(super().getState() - 1)
            if super().getState() < self.getWorkerCount() \
                    and queueLoader.getQueue() >= 2 \
                    and self.getNextElement().getState() < self.getNextElement().getWorkerCount():
                queueLoader.setQueue(queueLoader.getQueue() - 1)
                self.getNextElement().setState(self.getNextElement().getState() + 1)
                super().setState(super().getState() + 1)
                super().putTnext((super().getTcurr() + super().getDelay(), 'work'))
                self.passed += 1

            else:
                self.waitStart = super().getTcurr()
                self.blocked += 1
                if not super().getState() < self.getWorkerCount():
                    self.blocked_loader += 1
                if not queueLoader.getQueue() >= 2:
                    self.blocked_queue += 1
                if not self.getNextElement().getState() < self.getNextElement().getWorkerCount():
                    self.blocked_dumptruck += 1
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
        queueLoader = self if self.parallelLoader is None else self.parallelLoader
        self.stateSum += delta * super().getState()
        self.meanQueue = self.getMeanQueue() + queueLoader.getQueue() * delta

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


