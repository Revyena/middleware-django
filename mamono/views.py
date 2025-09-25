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

    # We use an @action because the primary key lookup is NOT a standard list or retrieve.
    @action(detail=False, methods=['get'])
    def lookup(self, request):
        entity_id = request.query_params.get('id')
        model_name = request.query_params.get('model')

        if not entity_id or not model_name:
            missing_param = 'id' if not entity_id else 'model'
            return Response(
                {"error": f"Missing required parameter: '{missing_param}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ModelClass = MODEL_MAPPING.get(model_name)
        if not ModelClass:
            return Response(
                {"error": f"Invalid model parameter: '{model_name}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            field_name = FIELD_MAPPING[ModelClass]
        except KeyError:
            return Response(
                {"error": f"Model '{model_name}' is not configured in FIELD_MAPPING."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        lookup_params = {field_name: entity_id}

        try:
            entity_instance = get_object_or_404(ModelClass, **lookup_params)

        except Exception as e:
            return Response(
                {"error": f"Lookup failed for entity ID: {entity_id}. Details: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        uuid_to_return = str(entity_instance.pk)

        return Response({
            "model": model_name,
            "id": entity_id,
            "uuid": uuid_to_return
        }, status=status.HTTP_200_OK)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer