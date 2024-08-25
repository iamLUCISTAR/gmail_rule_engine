"""
Default configurations for the application
"""

import logging
from sqlalchemy import create_engine

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", level=logging.INFO)
LOG = logging.getLogger("gmail_rule_engine")


DB_URL = "mysql+pymysql://root:localinstance@localhost:3306/mailengine"
SQL_ENGINE = create_engine(DB_URL)
