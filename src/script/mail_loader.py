"""
Script to fetch the mails using Gmail API.
Load the fetched data from the API to locally running db instance.

Run command: python3 src/script/mail_loader.py --clear True --limit 10
params: flush:- to drop the created table and recreate the table
        limit:- count limit to fetch from the Gmail API
"""

import sqlalchemy
import argparse
from src.config.base_config import SQL_ENGINE, LOG as logger, FETCH_LIMIT
from src.dao.models import EmailMaster, clean_db
from src.dao.dao_manager import DBManager
from src.entity.email_entity import EmailMasterEntity
from src.manager.gmail_manager import GmailFetcher


def execute(limit: int, clear: bool):
    """
    Function to fetch the mail data via Gmail API and load it in the db.
    :param limit
    :param clear
    :returns None
    """
    db_obj = None
    try:
        records = GmailFetcher().fetch(limit)
        logger.info(f"Email records fetched: {len(records)}")
        if clear:
            clean_db()
        db_obj = DBManager(SQL_ENGINE)
        for record in records:
            try:
                entity_obj = EmailMasterEntity(record)
                email_data_dict = {
                    "id": entity_obj.get_id(),
                    "thread_id": entity_obj.get_thread_id(),
                    "history_id": entity_obj.get_history_id(),
                    "from_mail": entity_obj.get_from_mail(),
                    "to_mail": entity_obj.get_to_mail(),
                    "received_date": entity_obj.get_received_date(),
                    "subject": entity_obj.get_subject(),
                    "body": entity_obj.get_body(),
                    "msg_size": entity_obj.get_msg_size()
                }
                db_obj.add_record(EmailMaster(**email_data_dict))
            except sqlalchemy.exc.DataError as e:
                logger.warning(f"Id {record.get('id')} ignored due to error: {e}")
            except sqlalchemy.exc.IntegrityError:
                logger.warning(f"Id: {record.get('id')} already exists")
            except Exception as e:
                logger.exception(f"Insertion error: {e} for ID {record.get('id')}")
        logger.info("Mail data from Gmail loaded successfully in the db")
    except Exception as e:
        logger.exception(f"Exception while running the script: {e}")
    finally:
        if db_obj:
            db_obj.close_session()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to fetch and load emails in the db.")
    parser.add_argument("--clear", type=bool, help="Specify True/False to clean the db",
                        required=False, default=False)
    parser.add_argument("--limit", type=int, help="Enter mail fetch limit. Default limit 100",
                        required=False, default=FETCH_LIMIT)
    args = parser.parse_args()
    execute(args.limit, args.clear)
