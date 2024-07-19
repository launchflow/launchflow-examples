from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import StorageUser
from .serializers import CreateUserSerializer, ListUsersResponse, UserResponse


@api_view(["GET"])
def list_users(request):
    storage_users = StorageUser.objects.all()
    serializer = ListUsersResponse(storage_users, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        storage_user = serializer.save()
        response_serializer = UserResponse(storage_user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def user_detail(request, user_id):
    try:
        storage_user = StorageUser.objects.get(pk=user_id)
    except StorageUser.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserResponse(storage_user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CreateUserSerializer(storage_user, data=request.data)
        if serializer.is_valid():
            storage_user = serializer.save()
            response_serializer = UserResponse(storage_user)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        storage_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
