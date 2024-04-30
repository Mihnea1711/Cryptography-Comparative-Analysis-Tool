import logging
from datetime import timedelta
from typing import Optional

from business.algorithm.IAlgorithm import IAlgorithm
from business.algorithm.pycryptography.aes import AESCipher_Cryptography
from business.algorithm.pycryptography.rsa import RSACipher_Cryptography
from business.framework.IFramework import ICryptoFramework
from persistence.database.sqlite.sqlite import SQLiteAgent
from persistence.models.models import Metadata
from persistence.models.orms import Algorithm
from utils.constants import AES_ALGORITHM, RSA_ALGORITHM

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PyCryptographyService(ICryptoFramework):
    def __init__(self, db_agent: SQLiteAgent):
        super().__init__(db_agent)
        self.algorithm: Optional[IAlgorithm] = None

    def set_algorithm(self, algorithm: Algorithm):
        if algorithm.algorithm_name == AES_ALGORITHM:
            self.algorithm = AESCipher_Cryptography(db_agent=self.get_db_agent(), algorithm_name=algorithm.algorithm_name)
        elif algorithm.algorithm_name == RSA_ALGORITHM:
            self.algorithm = RSACipher_Cryptography(db_agent=self.get_db_agent(), algorithm_name=algorithm.algorithm_name)
        else:
            raise ValueError("Algorithm has not been implemented by this framework yet.")

    def get_algorithm(self) -> IAlgorithm:
        return self.algorithm

    def encrypt_file(self, file_path: str, key: bytes) -> (timedelta, str):
        return self._process_file(file_path, self.algorithm, key, encrypt=True)

    def decrypt_file(self, file_path: str, key: bytes) -> (timedelta, Metadata):
        return self._process_file(file_path, self.algorithm, key, encrypt=False)