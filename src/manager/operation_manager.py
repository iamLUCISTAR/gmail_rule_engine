"""
Contains the actions for creating rules and applying actions on the filtered mails.
"""
from sqlalchemy import select
from src.dao.dao_manager import DBManager
from src.dao.models import EmailMaster
from src.config.base_config import SQL_ENGINE, LOG
from src.manager.gmail_manager import GmailActionExecutor


class OperationManager:
    def __init__(self, rules: list, condition: str, actions: list):
        self._rules = rules
        self._condition = condition
        self._actions = actions
        self._db_obj = DBManager(SQL_ENGINE)

    def perform_actions(self):
        try:
            consolidated_rules = None
            for rule in self._rules:
                if consolidated_rules is None:
                    consolidated_rules = rule.generate_condition()
                else:
                    consolidated_rules = consolidated_rules & (rule.generate_condition()) \
                        if self._condition == "all" \
                        else consolidated_rules | (rule.generate_condition())
            query = (select(EmailMaster).filter(consolidated_rules))
            query_result = self._db_obj.run_query(query)
            filtered_ids = [res[0].id for res in query_result]
            if len(filtered_ids) == 0:
                LOG.info("Zero matching records for the given query!!")
                return
            filtered_ids = list(set(filtered_ids))
            gmail_action_obj = GmailActionExecutor()
            for action in self._actions:
                try:
                    payload = action.payload
                    payload['ids'] = filtered_ids
                    gmail_action_obj.perform(payload)
                    LOG.info(f"{action.action_name} action performed for {len(filtered_ids)} records")
                except Exception as e:
                    LOG.error(f"Error occurred while performing action: {action.action_name}, error: {e}")
        except Exception:
            raise
        finally:
            self._db_obj.close_session()

