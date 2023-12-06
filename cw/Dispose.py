from queue import PriorityQueue
from random import random
from Element import Element

class Dispose(Element):
    def __init__(self, id):
        super().__init__(0, 0, id)
        super().putTnext((float('inf'), 'work'))

    def inAct(self):
        self.outAct()

    def outAct(self):
        super().outAct()

    def printInfo(self):
        super().printInfo()


