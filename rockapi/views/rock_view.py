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
        try:
            # Get an object instance of a rock type
            rock_type = Type.objects.get(pk=request.data["typeId"])

            # Create a rock object and assign it property values
            rock = Rock()
            rock.user = request.auth.user
            rock.weight = request.data["weight"]
            rock.name = request.data["name"]
            rock.type = rock_type
            rock.save()

            serialized = RockSerializer(rock, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response("", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """

        try:
            rock = Rock.objects.get(pk=pk)
            if rock.user.id == request.auth.user.id:
                rock.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("", status=status.HTTP_403_FORBIDDEN)
        except Rock.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
