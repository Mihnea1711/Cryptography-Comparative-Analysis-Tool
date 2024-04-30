from business.service.keygen import KeygenService
from business.service.performance import ApplicationService
from persistence.database.sqlite.sqlite import SQLiteAgent
from persistence.models.orms import Framework, Algorithm
from utils.constants import CRYPTODOME, AES_ALGORITHM, ALGORITHM_TYPE_SYMM, CryptoOperation, NATIVE_CRYPTOGRAPHY, RSA_ALGORITHM, ALGORITHM_TYPE_ASYMM, OpenSSL, \
    OPENSSL_KEYS_DIR, KEY_TYPE_SYMM, KEY_TYPE_PRIVATE, KEY_TYPE_PUBLIC
from utils.utility_functions import create_directory

file_path = "test.txt"

def encrypt(frm_id, alg_id, service, key):
    operation = CryptoOperation.ENCRYPT.value

    new_file_path = service.measure_algorithm_performance(frm_id, alg_id, file_path, operation, key)

    return new_file_path
def decrypt(frm_id, alg_id, service, key, encr_file_path):
    operation = CryptoOperation.DECRYPT.value

    new_file_path = service.measure_algorithm_performance(frm_id, alg_id, encr_file_path, operation, key)

    return new_file_path

def main_aes_cryptography():
    db_agent = SQLiteAgent()
    service = ApplicationService(db_agent)
    key_gen = KeygenService(db_agent)

    frmw = Framework(framework_id=1, framework_name=NATIVE_CRYPTOGRAPHY)
    service.set_framework(frmw)

    alg = Algorithm(algorithm_id=1, algorithm_name=AES_ALGORITHM, algorithm_type=ALGORITHM_TYPE_SYMM)
    service.set_algorithm(alg)

    key, same_key = key_gen.generate_keys(alg.algorithm_type)

    encr_file_path = encrypt(frmw.framework_id, alg.algorithm_id, service, key)

    decr_file_path = decrypt(frmw.framework_id, alg.algorithm_id, service, key, encr_file_path)

    print(decr_file_path)

def main_rsa_cryptography():
    db_agent = SQLiteAgent()
    service = ApplicationService(db_agent)
    key_gen = KeygenService(db_agent)

    frmw = Framework(framework_id=1, framework_name=NATIVE_CRYPTOGRAPHY)
    service.set_framework(frmw)

    alg = Algorithm(algorithm_id=1, algorithm_name=RSA_ALGORITHM, algorithm_type=ALGORITHM_TYPE_ASYMM)
    service.set_algorithm(alg)

    private_key, public_key = key_gen.generate_keys(alg.algorithm_type)

    encr_file_path = encrypt(frmw.framework_id, alg.algorithm_id, service, public_key)

    decr_file_path = decrypt(frmw.framework_id, alg.algorithm_id, service, private_key, encr_file_path)

    print(decr_file_path)

def main_aes_cryptodome():
    db_agent = SQLiteAgent()
    service = ApplicationService(db_agent)
    key_gen = KeygenService(db_agent)

    frmw = Framework(framework_id=1, framework_name=CRYPTODOME)
    service.set_framework(frmw)

    alg = Algorithm(algorithm_id=1, algorithm_name=AES_ALGORITHM, algorithm_type=ALGORITHM_TYPE_SYMM)
    service.set_algorithm(alg)

    pair_of_keys = key_gen.generate_keys(alg.algorithm_type)

    encr_file_path = encrypt(frmw.framework_id, alg.algorithm_id, service, pair_of_keys[0])

    decr_file_path = decrypt(frmw.framework_id, alg.algorithm_id, service, pair_of_keys[0], encr_file_path)

    print(decr_file_path)

def main_rsa_cryptodome():
    db_agent = SQLiteAgent()
    service = ApplicationService(db_agent)
    key_gen = KeygenService(db_agent)

    frmw = Framework(framework_id=1, framework_name=CRYPTODOME)
    service.set_framework(frmw)

    alg = Algorithm(algorithm_id=1, algorithm_name=RSA_ALGORITHM, algorithm_type=ALGORITHM_TYPE_ASYMM)
    service.set_algorithm(alg)

    private_key, public_key = key_gen.generate_keys(alg.algorithm_type)

    encr_file_path = encrypt(frmw.framework_id, alg.algorithm_id, service, public_key)

    decr_file_path = decrypt(frmw.framework_id, alg.algorithm_id, service, private_key, encr_file_path)

    print(decr_file_path)

def main_aes_openssl():
    db_agent = SQLiteAgent()
    service = ApplicationService(db_agent)
    key_gen = KeygenService(db_agent)

    frmw = Framework(framework_id=1, framework_name=OpenSSL)
    service.set_framework(frmw)

    alg = Algorithm(algorithm_id=1, algorithm_name=AES_ALGORITHM, algorithm_type=ALGORITHM_TYPE_SYMM)
    service.set_algorithm(alg)

    key, same_key = key_gen.generate_keys(alg.algorithm_type)

    encr_file_path = encrypt(frmw.framework_id, alg.algorithm_id, service, key)

    decr_file_path = decrypt(frmw.framework_id, alg.algorithm_id, service, key, encr_file_path)

    print(decr_file_path)
    
def main_rsa_openssl():
    db_agent = SQLiteAgent()
    service = ApplicationService(db_agent)
    key_gen = KeygenService(db_agent)
    create_directory(OPENSSL_KEYS_DIR)

    frmw = Framework(framework_id=1, framework_name=OpenSSL)
    service.set_framework(frmw)

    alg = Algorithm(algorithm_id=1, algorithm_name=RSA_ALGORITHM, algorithm_type=ALGORITHM_TYPE_ASYMM)
    service.set_algorithm(alg)

    private_key, public_key = key_gen.generate_keys(alg.algorithm_type)

    encr_file_path = encrypt(frmw.framework_id, alg.algorithm_id, service, public_key)

    decr_file_path = decrypt(frmw.framework_id, alg.algorithm_id, service, private_key, encr_file_path)

    print(decr_file_path)

def test_rsa_key_insertions():
    db_agent = SQLiteAgent()
    key_gen = KeygenService(db_agent)
    private_key, public_key = key_gen.generate_keys(ALGORITHM_TYPE_ASYMM)

    key_gen.save_key_pair_in_db(private_key, KEY_TYPE_PRIVATE, public_key, KEY_TYPE_PUBLIC, RSA_ALGORITHM, 1, ALGORITHM_TYPE_ASYMM)

def test_aes_key_insertions():
    db_agent = SQLiteAgent()
    key_gen = KeygenService(db_agent)
    key, _ = key_gen.generate_keys(ALGORITHM_TYPE_SYMM)

    key_gen.save_key_pair_in_db(key, KEY_TYPE_SYMM, key, KEY_TYPE_SYMM, AES_ALGORITHM, 1, ALGORITHM_TYPE_SYMM)

if __name__ == '__main__':
    pass