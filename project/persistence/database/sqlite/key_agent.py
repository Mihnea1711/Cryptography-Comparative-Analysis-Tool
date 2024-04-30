import logging
from typing import List, Optional, Type
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from persistence.models.orms import Key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLiteKeyOperations:
    def __init__(self, session: Session):
        self.session = session

    def insert_key(self, key_name, key_value, key_type):
        try:
            # Check if the key name is empty
            if not key_name:
                raise ValueError("Key name cannot be empty.")

            # Check if a key with the same name already exists
            existing_key = self.session.query(Key).filter_by(key_name=key_name).first()
            if existing_key:
                raise ValueError("Key with the same name already exists.")

            key_data = Key(
                key_name=key_name,
                key_value=key_value,
                key_type=key_type
            )

            # Add the key to the session and commit
            self.session.add(key_data)
            self.session.commit()

            logger.info("Key inserted successfully.")
            return key_data.key_id
        except IntegrityError:
            self.session.rollback()  # Rollback in case of errors
            logger.error("Integrity error occurred. Rollback performed.")
        except ValueError as ve:
            logger.error(f"Error: {ve}")

    def get_all_keys(self) -> List[Type[Key]]:
        try:
            keys = self.session.query(Key).all()
            return keys
        except Exception as e:
            logger.error(f"Error: {e}")
            return []

    def get_key_by_name(self, key_name: str) -> Optional[Type[Key]]:
        try:
            key = self.session.query(Key).filter_by(key_name=key_name).one()
            return key
        except NoResultFound:
            logger.info(f"No key found with the name '{key_name}'.")
            return None
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
