from abc import ABC, abstractmethod


class MazeGenerator(ABC):
    @classmethod
    @abstractmethod
    def create(cls, width, height, rand):
        pass
