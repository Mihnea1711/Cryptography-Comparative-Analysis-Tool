import logging

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from business.algorithm.IAlgorithm import IAlgorithm
from persistence.database.sqlite.sqlite import SQLiteAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSACipher_Cryptodome(IAlgorithm):
    def __init__(self, db_agent: SQLiteAgent, algorithm_name: str):
        super().__init__(db_agent, algorithm_name)

    def encrypt(self, plain_text: bytes, key: bytes) -> bytes:
        try:
            public_key = RSA.import_key(key)
            cipher = PKCS1_OAEP.new(public_key)
            return cipher.encrypt(plain_text)
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
            private_key = RSA.import_key(key)
            cipher = PKCS1_OAEP.new(private_key)
            return cipher.decrypt(cyphered_text)
        except ValueError as e:
            logger.error("RSA Decryption failed due to value error: %s", e)
            raise
        except TypeError as e:
            logger.error("RSA Decryption failed due to type error: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown RSA decryption error: %s", e)
            raise

