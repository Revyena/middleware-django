from django.contrib.auth.models import User
from django.db.models import Model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from mamono.models import DiscordLevel, DiscordUser, DiscordGuild
from mamono.serializers import UserSerializer, LevelSerializer

MODEL_MAPPING: dict[str, type[Model]] = {
    "DiscordUser": DiscordUser,
    "DiscordGuild": DiscordGuild,
}

FIELD_MAPPING: dict[type[Model], str] = {
    DiscordUser: "user",
    DiscordGuild: "guild",
}


class UUIDLookupViewSet(viewsets.ViewSet):
    """
    A ViewSet dedicated to dynamically looking up a model instance
    based on a string model name and a specific entity ID, then returning its PK (UUID/ID).
    """

    def retrieve(self, request, pk=None):
        model_name = request.query_params.get('model')

        if not model_name:
            return Response(
                {"error": "Missing required model parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ModelClass = MODEL_MAPPING.get(model_name)
        if not ModelClass:
            return Response(
                {"error": f"Invalid model parameter: '{model_name}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        field_name = FIELD_MAPPING.get(ModelClass)
        if not field_name:
            return Response(
                {"error": f"Model '{model_name}' is not configured in FIELD_MAPPING."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            entity_instance = get_object_or_404(ModelClass, **{field_name: pk})
        except Exception as e:
            return Response(
                {"error": f"Lookup failed for entity ID: {pk}. Details: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "model": model_name,
            "id": pk,
            "uuid": str(entity_instance.pk)
        }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LevelViewSet(viewsets.ModelViewSet):
    queryset = DiscordLevel.objects.all()
    serializer_class = LevelSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = "user_id"

    def get_queryset(self):
        guild_id = self.request.query_params.get('guild')
        if not guild_id:
            return DiscordLevel.objects.none()
        return DiscordLevel.objects.filter(guild_id=guild_id)


