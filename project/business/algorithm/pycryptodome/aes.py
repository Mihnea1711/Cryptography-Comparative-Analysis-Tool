import logging

from Crypto.Cipher import AES

from business.algorithm.IAlgorithm import IAlgorithm
from persistence.database.sqlite.sqlite import SQLiteAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AESCipher_Cryptodome(IAlgorithm):
    def __init__(self, db_agent: SQLiteAgent, algorithm_name: str):
        super().__init__(db_agent, algorithm_name)

    def encrypt(self, plain_text: bytes, key: bytes) -> bytes:
        try:
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(plain_text)
            return cipher.nonce + tag + ciphertext
        except ValueError as e:
            logger.error("AES Encryption failed due to ValueError: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown AES encryption error: %s", e)
            raise

    def decrypt(self, cyphered_text: bytes, key: bytes) -> bytes:
        try:
            nonce = cyphered_text[:16]
            tag = cyphered_text[16:32]
            ciphertext = cyphered_text[32:]
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError as e:
            logger.error("AES Decryption failed: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown AES decryption error: %s", e)
            raise