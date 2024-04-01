from abc import ABC, abstractmethod
import connection

class CommonDb(ABC):

    @abstractmethod
    def get(self, tableName, **condition):
        return;

    @abstractmethod
    def insert(self, insert_model):
        pass

    @abstractmethod
    def update(self, id, update_model):
        pass

    @abstractmethod
    def delete(self, id):
        pass