from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth.models import User
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def chathome(request):
    return Response("Welcome To chat 1337  page")

# def index(request):
#     return render(request, "index.html")

# def room(request, room    _name):
#     return render(request, "room.html", {"room_name": room_name})


# class UserListView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Fetch all users from the database
#         users = User.objects.all()

#         # Define the serializer inline
#         class UserSerializer(serializers.ModelSerializer):
#             class Meta:
#                 model = User
#                 fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        
#         # Serialize the user data
#         serializer = UserSerializer(users, many=True)

#         # Get the ID and username of the authenticated user
#         authenticated_user_id = request.user.id if request.user.is_authenticated else None
#         authenticated_user_name = request.user.username if request.user.is_authenticated else None

#         # Return the serialized data along with the authenticated user's ID and name
#         response_data = {
#             'authenticated_user_id': authenticated_user_id,
#             'authenticated_user_name': authenticated_user_name,
#             'users': serializer.data
#         }

#         return Response(response_data, status=status.HTTP_200_OK)