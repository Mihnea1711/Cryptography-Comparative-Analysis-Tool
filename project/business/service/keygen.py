import logging
import os
from datetime import datetime
from enum import Enum

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from persistence.database.sqlite.sqlite import SQLiteAgent
from persistence.models.orms import Algorithm
from utils.constants import ALGORITHM_TYPE_SYMM, ALGORITHM_TYPE_ASYMM, KEY_TYPE_PRIVATE, KEY_TYPE_PUBLIC

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeygenService:
    def __init__(self, db_agent: SQLiteAgent):
        self.db_agent = db_agent
        self.key_type = Enum("types", ['public', 'private'])

    def generate_keys(self, algorithm_type: str) -> (bytes, bytes):
        if algorithm_type == ALGORITHM_TYPE_SYMM:
            return self.generate_aes_keys()
        elif algorithm_type == ALGORITHM_TYPE_ASYMM:
            return self.generate_key_pair_rsa_openssl()
        else:
            raise ValueError("Invalid algorithm type specified.")

    @staticmethod
    def generate_aes_keys() -> (bytes, bytes):
        # temporarily it will do just fine
        key = os.urandom(32)
        return key, key  # 256-bit key

    @staticmethod
    def generate_key_pair_rsa_openssl() -> (bytes, bytes):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_key_pem, public_key_pem

    def save_key_pair_in_db(self, key_pair_tuple: tuple, algorithm: Algorithm):
        try:
            if algorithm.algorithm_type == ALGORITHM_TYPE_SYMM:
                # For symmetric keys, only insert one key into the database
                key_id = self.db_agent.key_operations.insert_key(
                    key_name=f"{self.generate_unique_key_name(algorithm.algorithm_name.lower())}",
                    key_value=key_pair_tuple[0],
                    key_type=None
                )

                self.db_agent.key_pair_operations.insert_key_pair(
                    first_key_id=key_id,
                    second_key_id=key_id,  # Both keys are the same for symmetric algorithms
                    algorithm_id=algorithm.algorithm_id,
                )
            elif algorithm.algorithm_type == ALGORITHM_TYPE_ASYMM:
                # For asymmetric keys, insert both keys into the database
                first_key_id = self.db_agent.key_operations.insert_key(
                    key_name=f"{self.generate_unique_key_name(algorithm.algorithm_name.lower())}_{KEY_TYPE_PRIVATE}",
                    key_value=key_pair_tuple[0],
                    key_type=KEY_TYPE_PRIVATE
                )
                second_key_id = self.db_agent.key_operations.insert_key(
                    key_name=f"{self.generate_unique_key_name(algorithm.algorithm_name.lower())}_{KEY_TYPE_PUBLIC}",
                    key_value=key_pair_tuple[1],
                    key_type=KEY_TYPE_PUBLIC
                )

                self.db_agent.key_pair_operations.insert_key_pair(
                    first_key_id=first_key_id,
                    second_key_id=second_key_id,
                    algorithm_id=algorithm.algorithm_id,
                )

            logger.info("Key pair saved successfully.")
        except Exception as e:
            logger.error("Error occurred while saving key pair: %s", e)
            raise


    @staticmethod
    def generate_unique_key_name(base_name: str) -> str:
        unique_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"{base_name}_{unique_id}"
