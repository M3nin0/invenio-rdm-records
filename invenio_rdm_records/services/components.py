# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM service components."""

from invenio_records_resources.services.records.components import \
    ServiceComponent
from marshmallow import ValidationError


class AccessComponent(ServiceComponent):
    """Service component for access integration."""

    def _validate_record_access(self, record):
        """Check if all entities referenced in record.access do exist."""
        errors = []

        for owner in record.access.owners:
            try:
                owner.resolve(raise_exc=True)
            except LookupError as e:
                errors.append(e)

        for grant in record.access.grants:
            try:
                grant.resolve_subject(raise_exc=True)
            except LookupError as e:
                errors.append(e)

        return errors

    def _populate_access_and_validate(self, identity, data, record, **kwargs):
        """Populate and validate the record's access field."""
        if "access" in data:
            # populate the record's access field with the data already
            # validated by marshmallow
            record.update({"access": data.get("access")})

        if record is not None and not record.access.owners and identity.id:
            # TODO can this even happen? isn't the min length 1 in marshmallow?
            record.access.owners.add({"user": identity.id})

        errors = self._validate_record_access(record)
        if errors:
            message = ", ".join([str(e) for e in errors])
            raise ValidationError(message, field_name="access")

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""
        self._populate_access_and_validate(identity, data, record, **kwargs)

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        self._populate_access_and_validate(identity, data, record, **kwargs)
