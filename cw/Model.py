from Loader import Loader
from DumpTruck import DumpTruck


class Model:
    def __init__(self, elements):
        self.list = elements
        self.tnext = 0.0
        self.tcurr = self.tnext

    def simulate(self, time):
        print("Elements:")
        for element in self.list:
            print("- {} (id {})".format(element.getName(), element.getId()))

        while self.tcurr < time:

            self.tnext = float('inf')
            eventId = 0
            for e in self.list:
                if e.getTnext() < self.tnext:
                    self.tnext = e.getTnext()
                    eventId = e.getId()

            print("\nEvent in {}\ntime: {:.4f}".format(self.list[eventId].getName(), self.tnext))
            for e in self.list:
                e.doStatistics(self.tnext - self.tcurr)

            self.tcurr = self.tnext
            for e in self.list:
                e.setTcurr(self.tcurr)

            self.list[eventId].outAct()
            for e in self.list:
                if e.getTnext() == self.tcurr:
                    e.outAct()
            self.printInfo()

        self.printResult()
        print("The simulation has ended!\n")

    def printInfo(self):
        for e in self.list:
            e.printInfo()

    def printResult(self):
        print("\n-------------RESULTS-------------")
        for e in self.list:
            e.printResult()
            if isinstance(e, Loader):
                p = e
                print("Mean length of queue = {:.3f}\nBlock probability = {:.3f}\nBlocked loader probability = {:.3f}\nBlocked queue probability = {:.3f}\nBlocked dumptruck probability = {:.3f}\nMean workload = {:.3f}\n".format(
                    p.getMeanQueue() / self.tcurr,
                    p.blocked / (p.blocked + p.passed),
                    p.blocked_loader / (p.blocked),
                    p.blocked_queue / (p.blocked),
                    p.blocked_dumptruck / (p.blocked),
                    p.stateSum / self.tcurr
                ))
            elif isinstance(e, DumpTruck):
                p = e
                print(
                    "Mean length of queue = {:.3f}\nMean workload = {:.3f}\n".format(
                        p.getMeanQueue() / self.tcurr,
                        p.stateSum / self.tcurr
                    ))
            else:
                print()


