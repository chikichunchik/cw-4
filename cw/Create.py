from queue import PriorityQueue
import random
from Element import Element


class Create(Element):
    def __init__(self, delay, workerCount, id):
        super().__init__(delay, workerCount, id)
        self.putTnext((0.0, 'work'))

    def outAct(self):
        super().outAct()
        self.putTnext((self.getTcurr() + self.getDelay(), 'work'))
        is_found = False
        sorted_list = self.getNextElement()
        sorted_list.sort(key=lambda x: x.getDelayMean())

        for i in range(len(sorted_list)):
            if sorted_list[i].getState() < sorted_list[i].workerCount:
                sorted_list[i].inAct()
                is_found = True
                break
        if not is_found:
            i = random.randint(0, len(sorted_list) - 1)
            sorted_list[i].inAct()

        super().popTnextQueue()


