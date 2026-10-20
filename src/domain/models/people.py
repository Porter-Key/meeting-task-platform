from __future__ import annotations

from django.db import models

from .base import ExistingTableModel


class Person(ExistingTableModel):
    email = models.TextField(primary_key=True)
    identity_type = models.CharField(max_length=40, default="alias")
    role = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    source = models.CharField(max_length=80, default="manual")
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "people"


class PersonAlias(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    alias = models.TextField()
    normalized_alias = models.TextField(unique=True)
    email = models.ForeignKey(Person, db_column="email", to_field="email", on_delete=models.SET_NULL, null=True, blank=True, related_name="aliases")
    source = models.CharField(max_length=80, default="manual")
    confidence = models.FloatField(default=1.0)
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "person_aliases"


class PersonEmailAlias(ExistingTableModel):
    id = models.CharField(max_length=120, primary_key=True)
    owner_email = models.ForeignKey(Person, db_column="owner_email", to_field="email", on_delete=models.CASCADE, related_name="owned_email_aliases")
    alias_email = models.ForeignKey(Person, db_column="alias_email", to_field="email", on_delete=models.CASCADE, related_name="alias_email_aliases")
    is_primary = models.BooleanField(default=False)
    source = models.CharField(max_length=80, default="manual")
    metadata_payload = models.JSONField(default=dict)

    class Meta(ExistingTableModel.Meta):
        db_table = "person_email_aliases"
