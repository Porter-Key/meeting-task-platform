from __future__ import annotations

from rest_framework import serializers

from domain.models.people import Person


class PersonDTO(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["email", "identity_type", "role", "is_active", "source", "metadata_payload"]
