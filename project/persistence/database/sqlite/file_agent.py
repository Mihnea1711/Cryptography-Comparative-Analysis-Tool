import logging
from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from persistence.models.orms import File
from utils.utility_functions import get_filename_from_path, get_file_size, generate_file_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLiteFileOperations:
    def __init__(self, session: Session):
        self.session = session

    def insert_file(self, file_path: str, algorithm_id: int) -> Optional[File]:
        try:
            # Create a new File object and add it to the session
            filename = get_filename_from_path(file_path)
            filesize = get_file_size(file_path)
            filehash = generate_file_hash(file_path)

            # Create a new File object with the provided attributes
            new_file = File(
                file_name=filename,
                file_path=file_path,
                file_size=filesize,
                file_hash=filehash,
                algorithm_id=algorithm_id
            )

            self.session.add(new_file)
            self.session.commit()

            logger.info("File inserted successfully.")
            return new_file

        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise FileNotFoundError(f"Error: {e}")
        except IntegrityError as e:
            # Handle the case where there's a conflict (e.g., file with the same path already exists)
            self.session.rollback()  # Rollback the transaction to avoid leaving the database in an inconsistent state
            logger.error(f"Integrity constraint error occurred: {e}")
            raise ValueError(f"Integrity constraint error occurred: {e}")
        except Exception as e:
            logger.error(f"Unknown error occurred: {e}")
            raise Exception(f"Unknown error occurred: {e}")

    def read_all_files(self) -> Optional[List[File]]:
        # Retrieve all files from the database
        return self.session.query(File).all() or None

    def read_file_by_id(self, file_id) -> Optional[File]:
        # Retrieve a file by its ID
        return self.session.query(File).filter(File.file_id == file_id).first()

    def read_file_by_path(self, file_path) -> Optional[File]:
        # Retrieve a file by its file_path
        return self.session.query(File).filter(File.file_path == file_path).first()

    def read_file_by_hash(self, file_hash) -> Optional[File]:
        # Retrieve a file by its file_path
        return self.session.query(File).filter(File.file_hash == file_hash).first()
