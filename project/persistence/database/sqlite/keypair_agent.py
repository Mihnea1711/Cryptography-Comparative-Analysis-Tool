import logging
from typing import Optional, Type, List
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from persistence.models.orms import KeyPair

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLiteKeyPairOperations:
    def __init__(self, session: Session):
        self.session = session

    def insert_key_pair(self, first_key_id, second_key_id, algorithm_id):
        try:
            # Check if both public and private keys are provided
            if not first_key_id or not second_key_id:
                raise ValueError("Both public and private keys are required.")

            # Check if algorithm id is provided
            if not algorithm_id:
                raise ValueError("Algorithm id is required.")

            key_pair_data = KeyPair(
                first_key_id=first_key_id,
                second_key_id=second_key_id,
                algorithm_id=algorithm_id
            )

            self.session.add(key_pair_data)
            self.session.commit()

            logger.info("Key pair inserted successfully.")
        except IntegrityError:
            self.session.rollback()
            logger.error("Integrity error occurred. Rollback performed.")
        except ValueError as ve:
            logger.error(f"Error: {ve}")

    def get_all_key_pairs(self) -> list[Type[KeyPair]]:
        try:
            key_pairs = self.session.query(KeyPair).all()
            return key_pairs
        except Exception as e:
            logger.error(f"Error: {e}")
            return []

    def get_key_pairs_by_algorithm_id(self, algorithm_id: str) -> Optional[List[Type[KeyPair]]]:
        try:
            key_pairs = self.session.query(KeyPair).filter_by(algorithm_id=algorithm_id).all()
            return key_pairs
        except NoResultFound:
            logger.info(f"No key pair found for the algorithm '{algorithm_id}'.")
            return None
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
