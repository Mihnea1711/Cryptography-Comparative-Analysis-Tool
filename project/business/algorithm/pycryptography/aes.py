import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from business.algorithm.IAlgorithm import IAlgorithm
from persistence.database.sqlite.sqlite import SQLiteAgent
from utils.utility_functions import generate_iv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AESCipher_Cryptography(IAlgorithm):
    def __init__(self, db_agent: SQLiteAgent, algorithm_name: str):
        super().__init__(db_agent, algorithm_name)

    def encrypt(self, plain_text: bytes, key: bytes) -> bytes:
        try:
            # Generate IV
            iv = generate_iv()

            if len(key) != 32:
                raise ValueError("AES key must be 256 bits (32 bytes) long")
            if len(iv) != 16:
                raise ValueError("IV must be 128 bits (16 bytes) long")

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            # Pad the plaintext
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(plain_text) + padder.finalize()

            # Encrypt the padded data
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

            # Prepend IV to the encrypted data
            encrypted_data_with_iv = iv + encrypted_data

            logger.info("AES Encryption successful")
            return encrypted_data_with_iv
        except ValueError as e:
            logger.error("AES Encryption failed due to ValueError: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown AES encryption error: %s", e)
            raise

    def decrypt(self, cyphered_text: bytes, key: bytes) -> bytes:
        try:
            # Extract IV and encrypted data
            iv = cyphered_text[:16]  # IV size is 16 bytes
            encrypted_data = cyphered_text[16:]

            if len(key) != 32:
                raise ValueError("AES key must be 256 bits (32 bytes) long")
            if len(iv) != 16:
                raise ValueError("IV must be 128 bits (16 bytes) long")

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            # Decrypt the ciphertext
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            # Remove the padding
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            data = unpadder.update(decrypted_data) + unpadder.finalize()

            logger.info("AES Decryption successful")
            return data
        except ValueError as e:
            logger.error("AES Decryption failed: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown AES decryption error: %s", e)
            raise