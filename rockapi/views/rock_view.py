from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rockapi.models import Rock, Type
from django.contrib.auth.models import User

class RockView(ViewSet):
    """Rock View Set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance 
        """
        return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request):
        try:
            # Retrieves all rock row objects
            rocks = Rock.objects.all()
            # Passes the list of rock row objects to serialize
            serializer = RockSerializer(rocks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

class RockTypeSerializer(serializers.ModelSerializer):
    """Serializes types related data of rocks

    Returns:
        Serialized property of types to be used in Rocks' expansion
    """
    class Meta:
        model = Type
        fields = ("label",)

class RockOwnerSerializer(serializers.ModelSerializer):
    """Serializes User Data related a Rock

    Returns:
        Serialized properties of the user object to be included in Rocks' expansion
    """
    class Meta:
        model = User
        fields = ("first_name", "last_name",)

class RockSerializer(serializers.ModelSerializer):
    """Serialized database row objects to JSON

    Returns:
        Response body to client in format modelled after Rock class
    """

    type = RockTypeSerializer(many=False)
    user = RockOwnerSerializer(many=False)

    class Meta:
        model = Rock
        # Fields are the keys that will be shown in the response bdy
        fields = ("id", "name", "weight", "user", "type")
