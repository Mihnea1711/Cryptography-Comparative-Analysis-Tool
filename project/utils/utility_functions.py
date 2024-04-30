import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_file_hash(file_path):
    """Generate a unique SHA-256 hash of a file including file metadata and salt."""
    sha256_hash = hashlib.sha256()

    # Include file content
    with open(file_path, 'rb') as file:
        chunk = file.read(4096)
        while chunk:
            sha256_hash.update(chunk)
            chunk = file.read(4096)

    # # Include file metadata: size and modification timestamp
    # file_stat = os.stat(file_path)
    # metadata = f"{file_stat.st_size}{file_stat.st_mtime}".encode()
    # sha256_hash.update(metadata)
    #
    # # Include a random salt
    # salt = secrets.token_bytes(16)  # Generate a 16-byte (128-bit) random salt
    # sha256_hash.update(salt)

    return sha256_hash.hexdigest()

def get_file_size(file_path: str) -> int:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    return os.path.getsize(file_path)

import os

def get_filename_from_path(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")
    return os.path.basename(file_path)

def get_directory_path(file_path: str) -> str:
    return os.path.dirname(file_path)

def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def generate_iv() -> bytes:
    return os.urandom(16)  # 128-bit IV

def save_file(file_path: str, data: bytes):
    try:
        if os.path.exists(file_path):
            logger.error(f"Error: File already exists at '{file_path}'. Cannot overwrite.")
            raise FileExistsError(f"Error: File '{file_path}' already exists.")

        with open(file_path, 'wb') as file:
            file.write(data)
        logger.info(f"File saved successfully: {file_path}")
    except FileExistsError as e:
        logger.error(f"Error: File already exists at '{file_path}'. Cannot overwrite.")
        raise
    except PermissionError as e:
        logger.error(f"Error: Permission denied to write to '{file_path}'.")
        raise
    except Exception as e:
        logger.error(f"Error: Unknown error occurred while saving file: {e}")
        raise

def append_metadata_to_file(file_path: str, metadata_json: str):
    try:
        with open(file_path, 'rb+') as file:
            file_content = file.read()
            file.seek(0)
            file.write(metadata_json.encode('utf-8') + b'\n' + file_content)
        logging.info(f"Metadata appended to file '{file_path}' successfully.")
    except FileNotFoundError as e:
        logging.error(f"Error: File '{file_path}' not found. {e}")
        raise
    except Exception as e:
        logging.error(f"Failed to append metadata to file '{file_path}': {e}")
        raise

def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"File '{file_path}' deleted successfully.")
    else:
        logger.error(f"File '{file_path}' does not exist.")

def create_directory(directory_path: str):
    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating directory '{directory_path}': {e}")




