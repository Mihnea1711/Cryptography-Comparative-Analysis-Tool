import os

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

from persistence.models.orms import Algorithm, Framework, Base

def delete_file(path):
        try:
            os.remove(path)
            print(f"Deleted file: {path}")
        except FileNotFoundError:
            print(f"File not found: {path}. No deletion made.")
        except PermissionError:
            print(f"No permission to delete file: {path}")
        except Exception as e:
            print(f"Error occurred while deleting file {path}: {e}")

def insert_initial_data(engine: Engine):
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()

    # delete everything
    # for table in reversed(Base.metadata.sorted_tables):
    #     session.execute(table.delete())

    # Insert algorithms
    rsa_algorithm = Algorithm(algorithm_name='RSA', algorithm_type='asymmetric')
    aes_algorithm = Algorithm(algorithm_name='AES', algorithm_type='symmetric')
    session.add_all([rsa_algorithm, aes_algorithm])

    # Insert frameworks
    openssl_framework = Framework(framework_name='OpenSSL')
    cryptography_framework = Framework(framework_name='PyCryptography')
    cryptodome_framework = Framework(framework_name='PyCryptodome')
    session.add_all([openssl_framework, cryptography_framework, cryptodome_framework])

    session.commit()
    session.close()


if __name__ == "__main__":
    db_path = "my_database.db"
    delete_file(db_path)

    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    insert_initial_data(engine)
