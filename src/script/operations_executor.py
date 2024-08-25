"""
Script to apply rule actions on the mails stored in db.
Perform actions on the filtered mails via API call to Gmail API services.

Run command: python3 src/scripts/operations_executor.py --json <path/to/jsonfile/>
params: json:- path to json file in which rules and conditions are specified
"""

import json
import argparse
from src.entity.operations_entity import Action, Field, Predicate, Rule
from src.manager.operation_manager import OperationManager
from src.config.base_config import LOG as logger


def execute(json_data):
    """
    Function to perform actions on the mail data stored in the db via Gmail API.
    :param json_data
    :returns None
    """
    try:
        for operation in json_data['operations']:
            try:
                rules_list = [Rule(Field(each_rule['field']), Predicate(each_rule['predicate']), each_rule['value'])
                              for each_rule in operation['rules']]
                actions_list = [Action(each_action) for each_action in operation['action']]
                OperationManager(rules_list, operation['condition'], actions_list).perform_actions()
                logger.info("Json rules processed successfully on the mails.")
            except ValueError as e:
                logger.warning(f"Value Error exception raised: {e}")
            except Exception as e:
                logger.exception(f"{operation} caused exception : {e}")
    except Exception as e:
        logger.exception(f"Exception while executing the script: {e}")


if __name__ == '__main__':
    with open('rules.json', 'r') as file:
        testcase_data = json.load(file)
    execute(testcase_data)
