from abc import abstractmethod, ABC

from persistence.database.sqlite.sqlite import SQLiteAgent


class IAlgorithm(ABC):
    def __init__(self, db_agent: SQLiteAgent, algorithm_name: str):
        self.__db_Agent = db_agent
        self.__algorithm_name = algorithm_name

    def get_algorithm_name(self) -> str:
        return self.__algorithm_name

    @abstractmethod
    def encrypt(self, plain_text: bytes, key: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, cyphered_text: bytes, key: bytes) -> bytes:
        pass