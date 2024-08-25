"""
Entity classes to store fields, predicates and rules for actions to be performed on the mails.
"""

from datetime import datetime, timedelta
from src.dao.models import EmailMaster
from src.config.base_config import TIME_ENTITIES, VALID_FIELDS, VALID_PREDICATES, DATE_FIELDS, DAYS_CONVERTER


class Field:
    """
    Entity class for fields.
    """
    def __init__(self, field):
        self._field_name = field
        self.__validate()

    @property
    def field_name(self):
        return self._field_name

    def __validate(self):
        if self._field_name not in VALID_FIELDS:
            raise ValueError(f"INVALID VALUE : Choose any one of the following values:- {VALID_FIELDS}")


class Predicate:
    """
    Entity class for predicates
    """
    def __init__(self, predicate):
        self.predicate_name = predicate
        self.__validate()
        self.method = getattr(self, predicate) if hasattr(self, predicate) else None

    def __validate(self):
        if self.predicate_name not in VALID_PREDICATES:
            raise ValueError(f"INVALID VALUE : Choose any one of the following values:- {VALID_PREDICATES}")

    def less_than(self, key, value, **kwargs):
        args = {kwargs["time_entity"]: value}
        bound_range = datetime.now().today() - timedelta(**args)
        return key > bound_range

    def greater_than(self, key, value, **kwargs):
        args = {kwargs["time_entity"]: value}
        bound_range = datetime.now().today() - timedelta(**args)
        print("******", bound_range, timedelta(**args))
        return key < bound_range

    def contains(self, key, value, **kwargs):
        return key.ilike(f"%{value}%")

    def equals(self, key, value, **kwargs):
        return key == value

    def not_equals(self, key, value, **kwargs):
        return key != value


class Action:
    """
    Entity class for actions
    """
    def __init__(self, action_type):
        self.action_name = action_type
        self.action_mapper = {
            "read": {"removeLabelIds": ["UNREAD"]},
            "unread": {"addLabelIds": ["UNREAD"]},
        }
        self.payload = None
        if self.action_mapper.get(self.action_name) is None:
            self.payload = {"addLabelIds": [self.action_name.upper()]}
        else:
            self.payload = self.action_mapper[self.action_name]


class Rule:
    """
    Entity class for rules
    """
    def __init__(self, field, predicate, value):
        self._field_obj = field
        self._predicate_obj = predicate
        self._value = value
        self._time_entity = None
        self._validate_and_convert()

    def _validate_and_convert(self):
        if self._field_obj.field_name in DATE_FIELDS:
            val = self._value.split(" ")
            self._value = int(val[0])
            self._time_entity = val[1]

            if self._time_entity not in TIME_ENTITIES:
                raise ValueError(f"INVALID VALUE : Give any one of the following values:- {TIME_ENTITIES}")

            self._value = self._value * DAYS_CONVERTER[self._time_entity]
            self._time_entity = "days"

    def generate_condition(self):
        key = EmailMaster.getattr(self._field_obj.field_name)
        statement = self._predicate_obj.method(key, self._value, time_entity=self._time_entity)
        return statement
