import logging

from cryptography.exceptions import InvalidKey, UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

from business.algorithm.IAlgorithm import IAlgorithm
from persistence.database.sqlite.sqlite import SQLiteAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSACipher_Cryptography(IAlgorithm):
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

            encrypted_data = public_key.encrypt(plain_text, padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))
            logger.info("RSA Encryption successful")
            return encrypted_data
        except ValueError as e:
            logger.error("Invalid PEM-encoded public key: %s", e)
            raise
        except TypeError as e:
            logger.error("Invalid type or backend: %s", e)
            raise
        except InvalidKey as e:
            logger.error("Invalid RSA public key: %s", e)
            raise
        except UnsupportedAlgorithm as e:
            logger.error("Unsupported algorithm: %s", e)
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

            decrypted_data = private_key.decrypt(cyphered_text, padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))
            logger.info("RSA Decryption successful")
            return decrypted_data
        except ValueError as e:
            logger.error("RSA Decryption failed due to value error: %s", e)
            raise
        except TypeError as e:
            logger.error("RSA Decryption failed due to type error: %s", e)
            raise
        except InvalidKey as e:
            logger.error("Invalid RSA private key: %s", e)
            raise
        except UnsupportedAlgorithm as e:
            logger.error("Unsupported algorithm: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown RSA decryption error: %s", e)
            raise

