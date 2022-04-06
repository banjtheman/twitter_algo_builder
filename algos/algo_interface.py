from abc import ABC, abstractmethod
from algo_builder.algorithm import Algorithm


class TwitterAlgorithm(ABC):
    @abstractmethod
    def define_algo(self) -> Algorithm:
        pass
