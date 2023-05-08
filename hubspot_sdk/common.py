from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    pass

from enum import StrEnum


class StandardObjects(StrEnum):
    COMPANY = 'companies'
    CONTACT = 'contacts'
    DEAL = 'deals'
    TICKET = 'tickets'


class PropertyType(StrEnum):
    BOOLEAN = 'bool'
    ENUMERATION = 'enumeration'
    DATE = 'date'
    DATETIME = 'datetime'
    STRING = 'string'
    NUMBER = 'number'


class FieldType(StrEnum):
    BOOLEAN = 'booleancheckbox'
    CALCULATION = 'calculation_equation'
    CHECKBOX = 'checkbox'
    DATE = 'date'
    FILE = 'file'
    NUMBER = 'number'
    RADIO = 'radio'
    DROPDOWN = 'select'
    TEXT = 'text'
    TEXTAREA = 'textarea'
