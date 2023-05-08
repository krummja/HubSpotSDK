from __future__ import annotations
from beartype.typing import *
if TYPE_CHECKING:
    pass

from devtools import debug

from hubspot_sdk.common import StandardObjects
from hubspot_sdk.common import PropertyType
from hubspot_sdk.common import FieldType
from hubspot_sdk.schema.builder import SchemaBuilder
from hubspot_sdk.schema.builder import SchemaDefinition
from hubspot_sdk.schema.builder import PropertyDefinition


def test_schema():

    test_property = PropertyDefinition(
        name="test_property",
        label="Test Property",
        property_type=PropertyType.STRING,
        field_type=FieldType.TEXT,
    )

    json = test_property.json()
    debug(json)


if __name__ == '__main__':
    test_schema()
