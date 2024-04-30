import os
from enum import Enum


class CryptoOperation(Enum):
    ENCRYPT = "encryption"
    DECRYPT = "decryption"

AES_ALGORITHM = "AES"
RSA_ALGORITHM = "RSA"

NATIVE_CRYPTOGRAPHY = "PyCryptography"
CRYPTODOME = "PyCryptodome"
OpenSSL = "OpenSSL"

ALGORITHM_TYPE_SYMM = "symmetric"
ALGORITHM_TYPE_ASYMM: str = "asymmetric"

KEY_TYPE_SYMM = "symmetric"
KEY_TYPE_PRIVATE = "private"
KEY_TYPE_PUBLIC = "public"

DATE_FORMAT = "%d/%m/%Y %H:%M:%S.%f"

METADATA_FILE_ID = "file_id"

PUBLIC_KEY_FILE_PATH = './opensslkeys/public_key.pem'
PRIVATE_KEY_FILE_PATH = './opensslkeys/private_key.pem'
OPENSSL_KEYS_DIR = os.path.dirname(PUBLIC_KEY_FILE_PATH)