from django.urls import path
from . import views , authentication_remote

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update/', views.update, name='update'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('verify_email/<uidb64>/<token>/',views.verify_email, name='verify_email'),
    path('reset-password/', views.reset_password, name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_user, name='reset_password'),
    path('otp/',views.otp, name='otp'),
    path('verify_account/<uidb64>/<token>/',views.verify_account, name='verify_account'),
    path('send_verification_email/',views.send_verification_email, name='send_verification_email'),
    path('verify_email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('active_2fa/',views.active_2fa, name='active_2fa'),
    ##############################View for friends##########################################
    path('send_friend_request/', views.send_friend_request, name='add_friend'),
    path('accept_friend_request/', views.accept_friend_request, name='accept_friend_request'),
    path('list_friends/', views.list_friends, name='list_friends'),
    path('list_requst_friend/', views.list_requst_friend, name='list_requst_friend'),
    path('search_friend/', views.search_friend, name='search_friend'), 
    path('remove_friend/', views.remove_friend, name='remove_friend'),
    ##############################View for authentication_remote##########################################
    path('update_username/',authentication_remote.update_username, name='update_username'),
    path('oauth/login/', authentication_remote.google_login, name='google_login'),
    path('oauth/callback/', authentication_remote.google_callback, name='google_callback'),
    path('authorize/', authentication_remote.authorize_42, name='authorize_42'),
    path('callback/', authentication_remote.callback_42, name='callback_42'),
]
# https://www.youtube.com/watch?v=gCDLNZB_FXc

# http://localhost:8000/login/

#    http://localhost:8000/oauth/callback// 
# {
# "username_friend":"KaaKALI"
# }



# new mesage

#modllwere
 
# build absolut url

# {
#     "email" : "maaloum.yassine@gmail.com",
#     "username" : "KaaKALI",
#     "first_name" : "kaaamal",
#     "last_name" : "kaaamal",
#     "password" : "A1A1A1",
#     "confirm_password" : "A1A1A1"
# }


# https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-48c20a1049615aa638dfa04140f65a2529efcc26099062bf5ca40d81afb5c191
# &redirect_uri=http://localhost:8080/profile/&response_type=code&scope=public


# http://127.0.0.1:8000/authorize/


# https://www.youtube.com/watch?v=Zo2Uupw2hNg

# {
#     "email" : "yassine@ll.com",
#     "password" : "MAALOUM0000#lv33"
# }

# {
#     "email" : "maaloum.yassine@gmail.com",
#     "password" : "MAALOUM0000#lv33"
# }
# {
#   "email" : "maaloum.yassine@gmail.com",
#   "username" : "ymaaaalouma",
#   "first_name" : "kaaamaal",
#   "last_name" : "kamaaaal1aaa",
#   "password" : "MAALOUM0000#lv33",
#   "confirm_password" : "MAALOUM0000#lv33"
# }
# {
# "email":"maaloum.yassine@gmail.com"
# }

# # lslsls


# {
# "username":"lslsls",
# "new_password":"0000",
# "confirm_password":"0000"
# }

# {
#     "email" : "maaloum.yassine@gmail.com",
#     "password" : "MAALOUM0000#lv33",
# }

# {
# "username":"lslsls",
# "password":"A0000"
# }

#listfriend avatar regler firstnane et lastname sockets pour online Redis 

# {
#     "email" : "badrsouhar@gmail.com",
#     "username" : "aaa",
#     "first_name" : "badr",
#     "last_name" : "souhar",
#     "password" : "Abadr2@ajg",
#     "confirm_password" : "Abadr2@ajg"
# }

# {
# "email" : "badrsouhar@gmail.com",
# "password" : "MAALOUM1111#lv33"
# }