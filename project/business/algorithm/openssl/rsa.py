import logging
import os
import subprocess

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

from business.algorithm.IAlgorithm import IAlgorithm
from persistence.database.sqlite.sqlite import SQLiteAgent
from utils.constants import PUBLIC_KEY_FILE_PATH, PRIVATE_KEY_FILE_PATH
from utils.utility_functions import file_exists, delete_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSACipher_OpenSSL(IAlgorithm):
    def __init__(self, db_agent: SQLiteAgent, algorithm_name: str):
        super().__init__(db_agent, algorithm_name)

    def encrypt(self, plain_text: bytes, key: bytes) -> bytes:
        try:
            public_key = serialization.load_pem_public_key(
                key,
                backend=default_backend()
            )

            if not isinstance(public_key, RSAPublicKey):
                raise ValueError("Invalid public key format")

            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            with open(PUBLIC_KEY_FILE_PATH, "wb") as f:
                f.write(public_key_pem)

            if not file_exists(PUBLIC_KEY_FILE_PATH):
                raise FileNotFoundError("PEM file containing public key does not exist.")

            openssl_cmd = f'openssl rsautl -encrypt -pubin -inkey {PUBLIC_KEY_FILE_PATH}'
            encrypted_data = subprocess.check_output(openssl_cmd.split(), input=plain_text)

            delete_file(PUBLIC_KEY_FILE_PATH)

            return encrypted_data
        except ValueError as e:
            logger.error("Invalid PEM-encoded public key: %s", e)
            raise
        except TypeError as e:
            logger.error("Invalid type or backend: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown RSA encryption error: %s", e)
            raise

    def decrypt(self, cyphered_text: bytes, key: bytes) -> bytes:
        try:
            private_key = serialization.load_pem_private_key(
                key, None,
                backend=default_backend()
            )

            if not isinstance(private_key, RSAPrivateKey):
                raise ValueError("Invalid private key format")

            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            with open(PRIVATE_KEY_FILE_PATH, "wb") as f:
                f.write(private_key_pem)

            if not file_exists(PRIVATE_KEY_FILE_PATH):
                raise FileNotFoundError("PEM file containing private key does not exist.")

            openssl_cmd = f'openssl rsautl -decrypt -inkey {PRIVATE_KEY_FILE_PATH}'
            decrypted_data = subprocess.check_output(openssl_cmd.split(), input=cyphered_text)

            delete_file(PRIVATE_KEY_FILE_PATH)

            return decrypted_data
        except ValueError as e:
            logger.error("RSA Decryption failed due to value error: %s", e)
            raise
        except TypeError as e:
            logger.error("RSA Decryption failed due to type error: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown RSA decryption error: %s", e)
            raise

