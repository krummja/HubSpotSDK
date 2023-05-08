from __future__ import annotations
from beartype.typing import *
if TYPE_CHECKING:
    pass

import yaml
import csv

from yaml import Loader
from pathlib import Path
from dataclasses import dataclass

from hubspot_sdk.common import StandardObjects
from hubspot_sdk.common import PropertyType
from hubspot_sdk.common import FieldType


@dataclass
class PropertyDefinition:
    name: str
    label: str
    property_type: PropertyType | str
    field_type: FieldType | str
    description: str | None = None
    group_name: str | None = None
    has_unique_value: bool = False
    hidden: bool = False
    primary: bool = False
    secondary: bool = False
    required: bool = False

    def json(self):
        if isinstance(self.property_type, PropertyType):
            _type = self.property_type.value
        else:
            _type = self.property_type

        if isinstance(self.field_type, FieldType):
            _field_type = self.field_type.value
        else:
            _field_type = self.field_type

        if self.primary:
            self.required = True
            self.has_unique_value = True

        if self.secondary:
            self.required = True

        return {
            "name": self.name,
            "label": self.label,
            "type": _type,
            "fieldType": _field_type,
            "description": self.description,
            "groupName": self.group_name,
            "hasUniqueValue": str(self.has_unique_value).lower(),
            "hidden": str(self.hidden).lower(),
            "isPrimaryDisplayLabel": str(self.primary).lower(),
        }


@dataclass
class SchemaDefinition:
    name: str
    singular: str = ''
    plural: str = ''

    @property
    def singular_label(self) -> str:
        if self.singular is not None:
            singular = self.singular
        else:
            singular = self.name.replace("_", " ")
        singular = singular.title()
        return singular

    @property
    def plural_label(self) -> str:
        plural = self.plural if self.plural else self.singular_label + "s"
        plural = plural.title()
        return plural

    def json(self):
        return {
            "name": self.name,
            "labels": {
                "singular": self.singular_label,
                "plural": self.plural_label,
            },
            "primaryDisplayProperty": None,
            "secondaryDisplayProperties": [],
            "requiredProperties": [],
            "searchableProperties": [],
            "properties": [],
            "associatedObjects": [],
        }


class SchemaBuilder:

    def __init__(self, schema_definition: SchemaDefinition) -> None:
        self.definition = schema_definition
        self.properties: list[dict[str, Any]] = []
        self.required_properties: list[str] = []
        self.primary_display_property: str | None = None
        self.secondary_display_properties: list[str] = []
        self.associations = []

    def add_property(self, property_definition: PropertyDefinition) -> None:
        property_dict = property_definition.json()

        is_primary = property_definition.primary
        is_secondary = property_definition.secondary
        is_required = property_definition.required

        if is_primary and self.primary_display_property is None:
            self.primary_display_property = property_dict.get('name')
        if is_secondary:
            self.secondary_display_properties.append(property_dict['name'])
        if is_required:
            self.required_properties.append(property_dict['name'])

        self.properties.append(property_dict)

    def add_association(self, object_type: StandardObjects | str) -> None:
        if isinstance(object_type, StandardObjects):
            self.associations.append(object_type.value)
        else:
            self.associations.append(object_type.upper())

    def build(self, with_props: bool = True) -> dict[str, Any]:
        schema = self.definition.json()
        schema['primaryDisplayProperty'] = self.primary_display_property

        secondary = schema.get('secondaryDisplayProperties', [])
        secondary.extend(self.secondary_display_properties)
        schema['secondaryDisplayProperties'] = secondary

        associations = schema.get('associatedObjects', [])
        associations.extend(self.associations)
        schema['associatedObjects'] = associations

        if with_props:
            properties = schema.get('properties', [])
            properties.extend(self.properties)
            schema['properties'] = properties

            required = schema.get('requiredProperties', [])
            required.extend(self.required_properties)
            schema['requiredProperties'] = required

        return schema

    def from_json(self, json_path: str) -> dict[str, Any]:
        return {}


class SchemaParser:

    def __init__(self, path: Path | str) -> None:
        self.path = path
        self.data = []

    def load_csv(self, filename: str) -> None:
        if isinstance(self.path, str):
            filepath = Path(self.path) / filename
        else:
            filepath = self.path / filename

        with open(str(filepath), mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.data = list(reader)
