from Create import Create
from Loader import Loader
from Dispose import Dispose
from Model import Model
from DumpTruck import DumpTruck

class SimModel:
    def __init__(self):
        self.TIME = 1000.0
        self.c = Create(delay=4, workerCount=1, id=0)
        self.c.setName("Creator")
        self.c.setDistribution("erlang")
        self.c.setDelayDev(2)
        self.c.putTnext((0, 'work'))

        self.p1 = Loader(delay=14, workerCount=1, prepareDelay=2, id=1)
        self.p1.setName("Loader1")
        self.p1.setMaxqueue(float('inf'))
        self.p1.setDistribution("exp")

        self.p2 = Loader(delay=12, workerCount=1, prepareDelay=2, id=2)
        self.p2.setName("Loader2")
        self.p2.setMaxqueue(float('inf'))
        self.p2.setDistribution("exp")

        self.p3 = DumpTruck(delay=[22, 2], workerCount=2, prepareDelay=14, id=3)
        self.p3.setName("DumpTruck")
        self.p3.setMaxqueue(float('inf'))
        self.p3.setDistribution(['norm', 'unif'])
        self.p3.setPrepareDelayDistribution('norm')
        self.p3.setPrepareDev(23)
        self.p3.setDelayDev([23, 8])

        self.d = Dispose(id=4)
        self.d.setName("Dispose")

        self.c.setNextElement([self.p1, self.p2])
        self.p1.setNextElement(self.p3)
        self.p2.parallelLoader = self.p1
        self.p2.setNextElement(self.p3)
        self.p3.setNextElement(self.d)
        self.list = []
        self.list.append(self.c)
        self.list.append(self.p1)
        self.list.append(self.p2)
        self.list.append(self.p3)
        self.list.append(self.d)

    def simulate(self):
        model = Model(self.list)
        model.simulate(self.TIME)


if __name__ == '__main__':
    model = SimModel()
    model.simulate()


