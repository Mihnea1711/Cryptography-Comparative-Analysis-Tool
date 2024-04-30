import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from persistence.models.orms import Framework, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLiteFrameworkOperations:
    def __init__(self, session: Session):
        self.session = session

    def insert_framework(self, framework_name):
        try:
            framework = Framework(framework_name=framework_name)
            self.session.add(framework)
            self.session.commit()
            logger.info("Framework inserted successfully.")
            return True, "Framework inserted successfully."
        except IntegrityError:
            self.session.rollback()
            logger.error("Framework insertion failed. Framework name already exists.")
            return False, "Framework insertion failed. Framework name already exists."

    def get_all_frameworks(self):
        frameworks = self.session.query(Framework).all()
        return frameworks