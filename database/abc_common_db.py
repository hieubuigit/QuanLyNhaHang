from abc import ABC, abstractmethod

class abcCommonDb(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get(self, **condition):
        pass

    @abstractmethod
    def insert(self, insert_model):
        pass

    @abstractmethod
    def update(self, id, update_model):
        pass

    @abstractmethod
    def delete(self, id):
        pass