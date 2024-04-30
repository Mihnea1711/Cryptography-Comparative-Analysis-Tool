import logging
from datetime import datetime
from typing import Optional, List

from business.algorithm.IAlgorithm import IAlgorithm
from business.framework.IFramework import ICryptoFramework
from business.framework.openssl import OpenSSLService
from business.framework.pycryptodome import PyCryptodomeService
from business.framework.pycryptography import PyCryptographyService
from persistence.database.sqlite.sqlite import SQLiteAgent
from persistence.models.models import Metadata
from persistence.models.orms import Framework, Algorithm, PerformanceMetrics, KeyPair
from utils.constants import NATIVE_CRYPTOGRAPHY, CRYPTODOME, OpenSSL, CryptoOperation, DATE_FORMAT
from utils.utility_functions import append_metadata_to_file, delete_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApplicationService:
    def __init__(self, db_agent: Optional[SQLiteAgent]):
        self._crypto_service: Optional[ICryptoFramework] = None
        self._db_agent = db_agent

    def log_performance(self, timestamp, time_taken, op_type, file_id, algorithm_id, framework_id):
        try:
            time_taken_ms = 1000 * time_taken
            self._db_agent.performance_operations.insert_performance(timestamp, time_taken_ms, op_type, file_id, algorithm_id, framework_id)
        except Exception as e:
            # Handle the exception here
            logger.error(f"Error occurred while logging performance: {e}")
            raise

    def set_framework(self, framework: Framework):
        if framework.framework_name == NATIVE_CRYPTOGRAPHY:
            self._crypto_service = PyCryptographyService(self._db_agent)
        elif framework.framework_name == CRYPTODOME:
            self._crypto_service = PyCryptodomeService(self._db_agent)
        elif framework.framework_name == OpenSSL:
            self._crypto_service = OpenSSLService(self._db_agent)
        else:
            raise ValueError("This framework has not been added yet.")

    def set_algorithm(self, algorithm: Algorithm):
        if self._crypto_service is None:
            raise ValueError("No framework set. Please set a framework first.")

        self._crypto_service.set_algorithm(algorithm)

    def get_crypto_service(self) -> Optional[ICryptoFramework]:
        return self._crypto_service

    def get_algorithm(self) -> IAlgorithm:
        return self._crypto_service.get_algorithm()

    def measure_algorithm_performance(self, framework_id: int, algorithm_id, file_path: str, operation: str, key: bytes):
        try:
            if self._crypto_service is None:
                raise ValueError("No framework set. Please set a framework")

            if operation == CryptoOperation.ENCRYPT.value:
                encrypted_file_path = ""
                try:
                    time_taken, encrypted_file_path = self._crypto_service.encrypt_file(file_path, key)
                    time_taken = round(time_taken, 3)
                    file = self._db_agent.file_operations.insert_file(file_path=encrypted_file_path, algorithm_id=algorithm_id)
                    metadata = Metadata(file_id=file.file_id)
                    append_metadata_to_file(encrypted_file_path, metadata.to_json())

                    # Log performance for encryption
                    timestamp_str = datetime.now().strftime(DATE_FORMAT)
                    timestamp = datetime.strptime(timestamp_str, DATE_FORMAT)
                    self.log_performance(timestamp, time_taken, operation, file.file_id, algorithm_id, framework_id)

                    logger.info("Encryption completed successfully. File encrypted and metadata appended. Filename: %s", encrypted_file_path)
                    return encrypted_file_path, time_taken * 1000
                except Exception as e:
                    logger.error("Error occurred during encryption: %s", e)
                    if encrypted_file_path:
                        delete_file(encrypted_file_path)
                    raise

            elif operation == CryptoOperation.DECRYPT.value:
                try:
                    time_taken, metadata, decrypted_file_path = self._crypto_service.decrypt_file(file_path, key)
                    time_taken = round(time_taken, 3)
                    timestamp_str = datetime.now().strftime(DATE_FORMAT)
                    timestamp = datetime.strptime(timestamp_str, DATE_FORMAT)

                    # Log performance for decryption
                    self.log_performance(timestamp, time_taken, operation, metadata.file_id, algorithm_id, framework_id)

                    logger.info("Decryption completed successfully. File decrypted. Filename: %s", decrypted_file_path)

                    return decrypted_file_path, time_taken * 1000
                except Exception as e:
                    logger.error("Error occurred during decryption: %s", e)
                    raise
            else:
                raise ValueError("Operation not supported.")
        except ValueError as ve:
            logger.error(ve)
            raise
        except Exception as e:
            logger.error("Error occurred: %s", e)
            raise

    def get_available_frameworks(self) -> List[Framework]:
        return self._db_agent.framework_operations.get_all_frameworks()

    def get_available_algorithms(self) -> List[Algorithm]:
        return self._db_agent.algorithm_operations.get_all_algorithms()

    def get_recorded_performances(self) -> List[PerformanceMetrics]:
        return self._db_agent.performance_operations.get_all_performances()

    def get_key_pairs_for_chosen_algorithm(self, algorithm_id: int) -> List[KeyPair]:
        return self._db_agent.key_pair_operations.get_key_pairs_by_algorithm_id(algorithm_id)


