"""
Contains models for the application
"""
from sqlalchemy import Column, String, Text, DateTime, BigInteger
from sqlalchemy.orm import declarative_base
from src.config.base_config import SQL_ENGINE, LOG as logger


Base = declarative_base()


def clean_db():
    """
    Function to drop the created table and recreate the table.
    """
    logger.info("Dropping all the created tables")
    Base.metadata.drop_all(SQL_ENGINE)
    logger.info("Recreating tables")
    Base.metadata.create_all(SQL_ENGINE)


class EmailMaster(Base):
    """
    table schema for the main table email_master
    """
    __tablename__ = 'email_master'
    id = Column(String(50), primary_key=True)
    thread_id = Column(String(50))
    history_id = Column(String(50))
    from_mail = Column(String(255), index=True)
    to_mail = Column(String(255), index=True)
    received_date = Column(DateTime, index=True)
    subject = Column(Text)
    body = Column(Text)
    msg_size = Column(BigInteger)

    @classmethod
    def getattr(cls, column_name: str):
        if cls.__dict__.get(column_name):
            return cls.__dict__.get(column_name)


Base.metadata.create_all(SQL_ENGINE)
