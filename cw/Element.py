import heapq
from FunRand import FunRand

class Element:
    def __init__(self, delay, workerCount, id):
        self.name = "Anonymous"
        self.quantity = 0
        self.tnext = []
        self.workerCount = workerCount
        self.delayMean = delay
        self.distribution = ""
        self.tcurr = 0.0
        self.state = 0
        self.queue = 0
        self.avgLoad = 0
        self.nextElement = None
        self.nextElementQueue = []
        self.nextRandomElement = {}
        self.nextElementType = 0
        self.id = id
        self.name = "element" + str(self.id)

    def getDelay(self):
        if self.getDistribution().lower() == "exp":
            delay = FunRand.Exp(self.getDelayMean())
        elif self.getDistribution().lower() == "norm":
            delay = FunRand.Norm(self.getDelayMean(), self.getDelayDev())
        elif self.getDistribution().lower() == "unif":
            delay = FunRand.Unif(self.getDelayMean(), self.getDelayDev())
        elif self.getDistribution().lower() == "erlang":
            delay = FunRand.Erlang(self.getDelayMean(), self.getDelayDev())
        else:
            delay = self.getDelayMean()

        return delay

    def getDelayDev(self):
        return self.delayDev

    def setDelayDev(self, delayDev):
        self.delayDev = delayDev

    def getDistribution(self):
        return self.distribution

    def setDistribution(self, distribution):
        self.distribution = distribution

    def getQuantity(self):
        return self.quantity

    def getTcurr(self):
        return self.tcurr

    def setTcurr(self, tcurr):
        self.tcurr = tcurr

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getNextElement(self):
        return self.nextElement

    def setNextElement(self, nextElement):
        self.nextElement = nextElement

    def nextElementType(self):
        return self.nextElementType

    def inAct(self):
        pass

    def outAct(self):
        self.quantity += 1

    def getTnext(self, full=False):
        if full:
            return min(self.tnext, key=lambda x: x[0])
        else:
            return min(self.tnext, key=lambda x: x[0])[0]

    def putTnext(self, tnext):
        heapq.heappush(self.tnext, tnext)

    def popTnextQueue(self):
        return heapq.heappop(self.tnext)

    def getDelayMean(self):
        return self.delayMean

    def setDelayMean(self, delayMean):
        self.delayMean = delayMean

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def printResult(self):
        print(self.getName() + " quantity = " + str(self.quantity))

    def updateAvgLoad(self):
        self.avgLoad = self.quantity / self.getTnext()

    def printInfo(self):
        if self.tnext[0] != float('inf'):
            self.updateAvgLoad()
        print("##### %s #####" % self.getName())
        if self.name == 'Dispose':
            print("quantity: %d" % self.quantity)
        else:
            print("state: %d | quantity: %d | queue: %d | tnext: %5.4f | avgLoad: %.4f" % (self.state, self.quantity, self.queue, self.getTnext(), self.avgLoad))

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def doStatistics(self, delta):
        pass

    def getQueue(self):
        return self.queue

    def setQueue(self, queue):
        self.queue = queue

    def getWorkerCount(self):
        return self.workerCount


