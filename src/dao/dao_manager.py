"""
Controller file for establishing db connection and query execution
"""

from sqlalchemy.orm import scoped_session, sessionmaker
from src.config.base_config import LOG as logger


class DBManager:
    """
    Class for creating database session and performing db operations.
    """

    def __init__(self, engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=self.engine)
        self.scoped_session_obj = scoped_session(self.session_factory)

    def add_record(self, model_instance: object):
        """
        Method to add data in the ORM model
        """
        session = self.scoped_session_obj()
        try:
            session.add(model_instance)
            session.commit()
        except Exception as e:
            logger.error(f"Error occurred while adding record in the table: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def run_query(self, statement):
        """
        Method to run query on the ORM model
        """
        session = self.scoped_session_obj()
        try:
            results = session.execute(statement).all()
            return results
        except Exception as e:
            logger.error(f"Error occurred while executing query in the table: {e}")
            raise
        finally:
            session.close()

    def close_session(self):
        """
        Method to close the db connection
        """
        logger.info("Removing the session and closing the db connection")
        self.scoped_session_obj.remove()
