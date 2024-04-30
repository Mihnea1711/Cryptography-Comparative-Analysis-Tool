import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime
from datetime import timedelta
from typing import Optional

from business.algorithm.IAlgorithm import IAlgorithm
from persistence.database.sqlite.sqlite import SQLiteAgent
from persistence.models.models import Metadata
from persistence.models.orms import Algorithm
from utils.utility_functions import file_exists, get_directory_path, save_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ICryptoFramework(ABC):
    def __init__(self, db_agent: SQLiteAgent):
        self.__algorithm: Optional[IAlgorithm] = None
        self.__db_agent = db_agent

    def get_db_agent(self) -> SQLiteAgent:
         return self.__db_agent

    @abstractmethod
    def set_algorithm(self, algorithm: Algorithm):
        pass

    @abstractmethod
    def get_algorithm(self) -> IAlgorithm:
        pass

    @abstractmethod
    def encrypt_file(self, file_path: str, key: bytes) -> (timedelta, str):
        pass

    @abstractmethod
    def decrypt_file(self, file_path: str, key: bytes) -> (timedelta, Metadata):
        pass

    @staticmethod
    def _process_file(file_path: str, algorithm: IAlgorithm, key: bytes, encrypt: bool):
        try:
            # Check if the file_path exists
            if not file_exists(file_path):
                raise FileNotFoundError(f"File '{file_path}' does not exist.")

            dir_path = get_directory_path(file_path)

            # Read file content
            with open(file_path, 'rb') as file:
                data = file.read()

            if encrypt:
                start_time = datetime.now()
                # Encrypt file data
                processed_data = algorithm.encrypt(plain_text=data, key=key)
                end_time = datetime.now()

                # Calculate time taken
                time_taken = (end_time - start_time).total_seconds()

                # Save the encrypted file
                encrypted_file_path = f"{algorithm.get_algorithm_name().lower()}_encrypted_{datetime.now().timestamp()}{os.path.splitext(file_path)[1]}"
                full_path = os.path.join(dir_path, encrypted_file_path)
                save_file(full_path, processed_data)

                return time_taken, full_path
            else:
                # Extract metadata from encrypted data
                metadata_end_index = data.find(b'\n')
                metadata_json = data[:metadata_end_index].decode('utf-8')
                metadata = Metadata.from_json(metadata_json)

                start_time = datetime.now()
                # Decrypt file data
                processed_data = algorithm.decrypt(cyphered_text=data[metadata_end_index + 1:], key=key)
                end_time = datetime.now()

                # Calculate time taken
                time_taken = (end_time - start_time).total_seconds()

                # Save the decrypted file
                decrypted_file_path = f"{algorithm.get_algorithm_name().lower()}_decrypted_{datetime.now().timestamp()}{os.path.splitext(file_path)[1]}"
                full_path = os.path.join(dir_path, decrypted_file_path)
                save_file(full_path, processed_data)

                return time_taken, metadata, full_path
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: {e}")
        except Exception as e:
            raise Exception(f"Processing failed: {e}")

