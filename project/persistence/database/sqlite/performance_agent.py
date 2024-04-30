import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from persistence.models.orms import PerformanceMetrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLitePerformanceOperations:
    def __init__(self, session: Session):
        self.session = session

    def insert_performance(self, timestamp, time_taken, op_type, file_id, algorithm_id, framework_id):
        try:
            performance = PerformanceMetrics(
                timestamp=timestamp,
                time=time_taken,
                op_type=op_type,
                file_id=file_id,
                algorithm_id=algorithm_id,
                framework_id=framework_id
            )
            self.session.add(performance)
            self.session.commit()
            logger.info("Performance metrics inserted successfully.")
        except IntegrityError:
            self.session.rollback()
            logger.error("Performance metrics insertion failed. Possible duplicate entry.")
            raise Exception("Performance metrics insertion failed. Possible duplicate entry.")

    def get_all_performances(self):
        try:
            metrics = self.session.query(PerformanceMetrics).all()
            return metrics
        except Exception as e:
            logger.error(f"Error fetching all performances: {e}")
            return []

    def get_all_sorted_by_timestamp(self):
        try:
            metrics = self.session.query(PerformanceMetrics).order_by(PerformanceMetrics.timestamp).all()
            return metrics
        except Exception as e:
            logger.error(f"Error fetching performances sorted by timestamp: {e}")
            return []

    def get_all_by_algorithm(self, algorithm_id):
        try:
            metrics = self.session.query(PerformanceMetrics).filter_by(algorithm_id=algorithm_id).all()
            return metrics
        except Exception as e:
            logger.error(f"Error fetching performances by algorithm: {e}")
            return []
