import logging
import subprocess

from Crypto.Cipher import AES

from business.algorithm.IAlgorithm import IAlgorithm
from persistence.database.sqlite.sqlite import SQLiteAgent
from utils.utility_functions import generate_iv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AESCipher_OpenSSL(IAlgorithm):
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

            openssl_cmd = [
                'openssl',
                'enc',
                '-nosalt',
                '-aes-256-cbc',
                '-K', key.hex(),
                '-iv', iv.hex(),
            ]

            process = subprocess.Popen(openssl_cmd, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            encrypted_data, error_output = process.communicate(input=plain_text)

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

            openssl_cmd = f'openssl enc -d -aes-256-cbc -K {key.hex()} -iv {iv.hex()}'
            decrypted_data = subprocess.check_output(openssl_cmd.split(), input=encrypted_data)

            return decrypted_data
        except ValueError as e:
            logger.error("AES Decryption failed: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown AES decryption error: %s", e)
            raise