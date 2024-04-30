from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, CheckConstraint, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class File(Base):
    __tablename__ = 'file'

    file_id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    file_hash = Column(String, unique=True)
    algorithm_id = Column(Integer, ForeignKey('algorithm.algorithm_id'))

    # Define a composite unique constraint
    __table_args__ = (
        UniqueConstraint('file_path', 'file_hash', 'algorithm_id'),
    )

    algorithm = relationship("Algorithm", back_populates="files")
    performances = relationship("PerformanceMetrics", back_populates="file")

    def __str__(self):
        return f"File(file_id={self.file_id}, file_name='{self.file_name}', file_path='{self.file_path}', file_size={self.file_size}, file_hash='{self.file_hash}')"
    def __repr__(self):
        return f"File(file_id={self.file_id}, file_name='{self.file_name}', file_path='{self.file_path}', file_size={self.file_size}, file_hash='{self.file_hash}')"


class Key(Base):
    __tablename__ = 'key'

    key_id = Column(Integer, primary_key=True)
    key_name = Column(String)
    key_value = Column(String)
    key_type = Column(Enum('public', 'private', name='key_type_enum'), nullable=True)

    def __str__(self):
        return f"Key(key_id={self.key_id}, key_name='{self.key_name}', key_value='{self.key_value}', key_type='{self.key_type}')"


class Algorithm(Base):
    __tablename__ = 'algorithm'

    algorithm_id = Column(Integer, primary_key=True)
    algorithm_name = Column(String, unique=True)
    algorithm_type = Column(String)

    __table_args__ = (
        CheckConstraint("algorithm_type IN ('symmetric', 'asymmetric')"),
    )

    files = relationship("File", back_populates="algorithm")
    key_pairs = relationship("KeyPair", back_populates="algorithm")

    def __str__(self):
        return f"Algorithm(algorithm_id={self.algorithm_id}, algorithm_name='{self.algorithm_name}', algorithm_type='{self.algorithm_type}')"


class PerformanceMetrics(Base):
    __tablename__ = 'performance_metrics'

    performance_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, unique=True)
    time = Column(Integer)
    op_type = Column(Enum('encryption', 'decryption', name='operation_type_enum'))
    file_id = Column(Integer, ForeignKey('file.file_id'))
    algorithm_id = Column(Integer, ForeignKey('algorithm.algorithm_id'))
    framework_id = Column(Integer, ForeignKey('framework.framework_id'))

    file = relationship("File", back_populates="performances")
    algorithm = relationship("Algorithm")
    framework = relationship("Framework")

    __table_args__ = (
        UniqueConstraint('timestamp', 'file_id', 'algorithm_id', 'framework_id', name='_timestamp_file_algorithm_framework_uc'),
    )

    def __str__(self):
        return f"PerformanceMetrics(performance_id={self.performance_id}, timestamp={self.timestamp}, time={self.time}, op_type='{self.op_type}')"


class Framework(Base):
    __tablename__ = 'framework'

    framework_id = Column(Integer, primary_key=True)
    framework_name = Column(String, unique=True)

    __table_args__ = (
        UniqueConstraint('framework_name'),
    )

    def __str__(self):
        return f"Framework(framework_id={self.framework_id}, framework_name='{self.framework_name}')"


class KeyPair(Base):
    __tablename__ = 'key_pairs'

    pair_id = Column(Integer, primary_key=True)
    first_key_id = Column(Integer, ForeignKey('key.key_id'))
    second_key_id = Column(Integer, ForeignKey('key.key_id'))
    algorithm_id = Column(Integer, ForeignKey('algorithm.algorithm_id'))

    algorithm = relationship("Algorithm", back_populates="key_pairs")
    first_key = relationship("Key", foreign_keys=[first_key_id], backref="first_key_pairs")
    second_key = relationship("Key", foreign_keys=[second_key_id], backref="second_key_pairs")

    def __str__(self):
        return f"KeyPair(pair_id={self.pair_id}, first_key_id={self.first_key_id}, second_key_id={self.second_key_id}, algorithm_id={self.algorithm_id})"

