from abc import ABC, abstractmethod


class SearchStrategy(ABC):
    @abstractmethod
    def apply(self, query, value):
        pass
