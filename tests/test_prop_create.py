from __future__ import annotations
from beartype.typing import *
if TYPE_CHECKING:
    pass

from dotenv import load_dotenv

import os
import json
from devtools import debug

from hubspot_sdk.common import PropertyType
from hubspot_sdk.common import FieldType
from hubspot_sdk.schema.builder import PropertyDefinition
from hubspot_sdk.context import HubSpotContext


load_dotenv()


def test_main():

    HS_API_KEY = os.environ['HS_API_KEY']

    test_property = PropertyDefinition(
        name="test_property",
        label="Test Property",
        property_type=PropertyType.STRING,
        field_type=FieldType.TEXT,
        group_name="contactinformation",
    )

    debug(test_property.json())

    with HubSpotContext(HS_API_KEY) as hs:
        response = hs.post(
            url='/crm/v3/properties/contacts',
            data=json.dumps(test_property.json()),
        )

        debug(response.json())


if __name__ == '__main__':
    test_main()
