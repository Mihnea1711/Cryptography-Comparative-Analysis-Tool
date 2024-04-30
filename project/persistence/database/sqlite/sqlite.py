import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from persistence.database.sqlite.algorithm_agent import SQLiteAlgorithmOperations
from persistence.database.sqlite.file_agent import SQLiteFileOperations
from persistence.database.sqlite.framework_agent import SQLiteFrameworkOperations
from persistence.database.sqlite.key_agent import SQLiteKeyOperations
from persistence.database.sqlite.keypair_agent import SQLiteKeyPairOperations
from persistence.database.sqlite.performance_agent import SQLitePerformanceOperations
from persistence.models.orms import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLiteAgent:
    def __init__(self, db_name='my_database.db'):
        self.db_name = db_name
        self.engine = None
        self.session = None
        self.file_operations = None
        self.key_operations = None
        self.algorithm_operations = None
        self.performance_operations = None
        self.framework_operations = None
        self.key_pair_operations = None

        # Establish the database connection and initialize helper classes
        self.init_database()

    def init_database(self):
        try:
            self.engine = create_engine(f'sqlite:///{self.db_name}')
            Base.metadata.create_all(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            # Initialize helper classes
            self.file_operations = SQLiteFileOperations(self.session)
            self.key_operations = SQLiteKeyOperations(self.session)
            self.algorithm_operations = SQLiteAlgorithmOperations(self.session)
            self.performance_operations = SQLitePerformanceOperations(self.session)
            self.framework_operations = SQLiteFrameworkOperations(self.session)
            self.key_pair_operations = SQLiteKeyPairOperations(self.session)

            logger.info("SQLite database connection established and helper classes initialized.")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            exit(1)

    def close_connection(self):
        try:
            if self.session:
                self.session.close_all()
            if self.engine:
                self.engine.dispose()
            logger.info("SQLite database connection closed.")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
