import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from persistence.models.orms import Algorithm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLiteAlgorithmOperations:
    def __init__(self, session: Session):
        self.session = session

    def insert_algorithm(self, algorithm_name, algorithm_type):
        algorithm = Algorithm(algorithm_name=algorithm_name, algorithm_type=algorithm_type)
        self.session.add(algorithm)
        try:
            self.session.commit()
            logger.info("Algorithm inserted successfully.")
            return True, "Algorithm inserted successfully."
        except IntegrityError:
            self.session.rollback()
            logger.error("Algorithm insertion failed. Algorithm name already exists.")
            return False, "Algorithm insertion failed. Algorithm name already exists."

    def get_all_algorithms(self):
        algorithms = self.session.query(Algorithm).all()
        return algorithms
