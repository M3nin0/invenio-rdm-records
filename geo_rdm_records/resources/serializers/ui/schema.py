# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Geo Secretariat.
#
# geo-rdm-records is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from marshmallow import fields

from invenio_rdm_records.resources.serializers.ui.schema import VocabularyL10Schema
from invenio_rdm_records.resources.serializers.ui import (
    UIObjectSchema as UIObjectSchemaBase,
)

#
# Schema
#
class UIObjectSchema(UIObjectSchemaBase):
    """Schema for dumping extra information for the UI."""

    geo_work_programme_activity = fields.Nested(
        VocabularyL10Schema, attribute="metadata.geo_work_programme_activity"
    )

    target_audiences = fields.List(
        fields.Nested(VocabularyL10Schema),
        attribute="metadata.target_audiences",
    )

    engagement_priorities = fields.List(
        fields.Nested(VocabularyL10Schema),
        attribute="metadata.engagement_priorities",
    )
