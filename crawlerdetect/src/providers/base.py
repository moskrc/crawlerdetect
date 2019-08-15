from abc import ABC, abstractmethod


class AbstractProvider(ABC):
    """
    Base provider interface
    """

    @abstractmethod
    def getAll(self):
        pass
