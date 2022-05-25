from abc import ABC, abstractmethod
from typing import List

import traci


class State(ABC):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context) -> None:
        self._context = context

    @abstractmethod
    def setContext(self, context): pass

    @abstractmethod
    def get_reading(self) -> list | None: pass


class Active(State):
    def __init__(self):
        self._name = 'Active'

    def setContext(self, context):
        self.context = context
        self.context.subscribe()

    def get_reading(self):
        return traci.inductionloop.getSubscriptionResults(self.context._id)[23]


class Faulty(Active):
    def __init__(self):
        self.name = 'Faulty'

    def setContext(self, context):
        return super().setContext(context)

    def get_reading(self):
        reading = traci.inductionloop.getSubscriptionResults(self.context._id)[
            23]
        try:
            l = list(reading[0])
            l[1] = 7.0
            reading[0] = tuple(l)
        except:
            pass
        return reading


class InActive(State):
    def __init__(self):
        self._name = 'InActive'

    def setContext(self, context):
        self.context = context
        self.context.unsubscribe()

    def get_reading(self): pass
