"""
Default configurations for the application
"""

import logging
from sqlalchemy import create_engine

# logger configs
logging.basicConfig(format="%(asctime)s---%(levelname)s---%(name)s: %(message)s", level=logging.INFO)
LOG = logging.getLogger("gmail_rule_engine")

# db configs
DB_URL = "mysql+pymysql://root:localinstance@localhost:3306/mailengine"
SQL_ENGINE = create_engine(DB_URL)

# rule engine configs
TIME_ENTITIES = ["day", "week", "month", "days", "weeks", "months"]
VALID_FIELDS = ["from_mail", "to_mail", "subject", "body", "received_date"]
VALID_PREDICATES = ["less_than", "greater_than", "equals", "not_equals", "contains"]
DATE_FIELDS = ["received_date"]
DAYS_CONVERTER = {
    "weeks": 7,
    "week": 7,
    "months": 30,
    "month": 30,
    "days": 1,
    "day": 1
}
