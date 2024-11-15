# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    # path("", views.index, name="index"),
	# path("<str:room_name>/", views.room, name="room"),
	path("", views.chathome, name="chathome"),
	# path("users/", views.UserListView.as_view(), name="user-list"),
]

# export $(cat .env | xargs)
