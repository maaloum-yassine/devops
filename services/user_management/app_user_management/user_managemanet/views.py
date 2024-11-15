from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from . import utils, models, serializers , redis_config
import redis , json, uuid, jwt , requests

#CLEAN CODE AND MIDLWERE AND CREATE APPLICATION WITH CONTAINER WITH REDIS AND POSTGRESS AND CLEAN RESPONSE

#************************************************HOME****************************************************************#


@api_view(['GET'])
def home(request:Request):
    if request.user.is_anonymous:
        return Response("Welcome To home 1337  page")
    return redirect('profile')

def generate_verification_token(user, flag):
    if flag is True:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
    else :
        uid = urlsafe_base64_encode(force_bytes(user.username))
    token = default_token_generator.make_token(user)
    return token, uid

def save_user_in_redis(user_data):
    user_key = f"user:{user_data['username']}"
    redis_config.redis_client.set(user_key, json.dumps(user_data), ex=3600)


#************************************************SIGN_UP****************************************************************#

@api_view(['POST', 'GET'])
def signup(request:Request):
    serializer = serializers.CustomUserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        fake_user = models.CustomUser(**validated_data)
        token , uid = generate_verification_token(fake_user, False)
        # token = default_token_generator.make_token(fake_user)
        # uid = urlsafe_base64_encode(force_bytes(fake_user.username))
        print("SEND EMAILLLLLLL")
        save_user_in_redis(validated_data)
        verification_link = f"http://localhost:8000/verify_account/{uid}/{token}/"
        html_message = render_to_string('verify_compte_template.html', {
            'reset_link': verification_link,
        })
        utils.send_email(validated_data['email'], html_message, False)
        return Response({"message": "Registration successful. Please check your email."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def verify_account(request: Request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user_data = redis_config.redis_client.get(f"user:{uid}")
        if user_data is None:
            return Response("Utilisateur introuvable ou le lien a expiré.", status=status.HTTP_400_BAD_REQUEST)
        user_data = json.loads(user_data)
        fake_user = models.CustomUser(**user_data)
    except (TypeError, ValueError, OverflowError):
        return Response({"error": "Lien invalide ou corrompu."}, status=status.HTTP_400_BAD_REQUEST)
    if default_token_generator.check_token(fake_user, token):
        user_data['is_email_verified'] = True
        user_data['active_2fa'] = False
        models.CustomUser.objects.create(**user_data)
        print("Account successfully created")
        redis_config.redis_client.delete(f"user:{uid}")
        return Response({"message": "Votre e-mail a été vérifié avec succès et votre compte est enregistré."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Le lien de vérification est invalide ou a expiré."}, status=status.HTTP_400_BAD_REQUEST)

#**************************************************************************************************************#

#*********************************************UPDATE**************************************************************#

@api_view(['PUT'])
def update(request:Request):
    if request.method == "GET":
        if request.user.is_anonymous:
            return redirect('home')
    user = request.user
    if request.data:
        serializer = serializers.CustomUserUpdateSerializer(request.user , data=request.data, partial=True)
        if serializer.is_valid():
            new_email = request.data.get("email")
            if new_email and new_email != user.email:
                user.is_email_verified = False
                user.active_2fa = False
                user.save()
            serializer.save()
            token = utils.generate_token(user, True)
            response = Response({
                "message": "update successful",
                "jwt": token
            }, status=status.HTTP_200_OK)
            response.set_cookie(key='jwt', value=token, httponly=True, secure=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "aucun element changer"}, status=status.HTTP_400_BAD_REQUEST)

#*********************************************UPLOAD-IMAGE*****************************************************************#

@api_view(['POST', 'GET'])
def upload_avatar(request:Request):
    if request.user.is_anonymous:
            return redirect('home')
    print(request.data)
    file = request.FILES.get('avatar')
    if not file:
        return Response({"error": "Aucune image fournie"}, status=status.HTTP_400_BAD_REQUEST)
    fs = FileSystemStorage(location='media/avatars/')
    filename = fs.save(file.name, file)
    file_url = fs.url(filename)
    user = request.user
    user.avatar = f"avatars/{filename}"
    user.save()
    return Response({"avatar_url": file_url}, status=status.HTTP_201_CREATED)

#*********************************************************************************************************************************#

#**************************************************ACTIVAE 2FA************************************************************#
@api_view(['POST', 'GET'])
def active_2fa(request:Request):
    if request.method == "GET":
        if request.user.is_anonymous:
            return redirect('home')
    if request.method == "POST":
        user = request.user
        if 'active_2fa' in request.data:
            if request.data['active_2fa'] == "true":
                if user.is_email_verified is True:
                    user.active_2fa = True
                    user.save()
                    return Response({"message": "2FA is active"}, status=status.HTTP_200_OK)
                else :
                        reponse = Response()
                        reponse = redirect('send_verification_email')
                        return reponse
            user.active_2fa = False
            user.save()
    return Response({"message": "2FA is not active"}, status=status.HTTP_200_OK)



@api_view(['GET'])
def send_verification_email(request):
    try:
        token , uid = generate_verification_token(request.user, True)
        verification_link = f"http://localhost:8000/verify_email/{uid}/{token}/"
        html_message = render_to_string('verify_email_template.html', {
            'verification_link': verification_link,
        })
        utils.send_email(request.user.email, html_message, False)
        print(f"{request.user.email}")
        return Response({"message": "A verification email has been sent."}, status=status.HTTP_200_OK)
    except models.CustomUser.DoesNotExist:
        return Response({"error": "This email does not exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.active_2fa = True
            user.save()
            return Response({"message": "Your email has been successfully verified."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "The verification link is invalid."}, status=status.HTTP_400_BAD_REQUEST)
    except models.CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#**************************************************************************************************************#

#**************************************RESET_PASSWORD**************************************************************#

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    try:
        user = models.CustomUser.objects.get(email=email)
        token , uid = generate_verification_token(user, True)
        reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"
        html_message = render_to_string('email_template.html', {
            'reset_link': reset_link,
        })
        utils.send_email(user.email, html_message, True)
        user.set_password_reset_token_expiration()
        user.save()
        return Response({"message": "A reset email has been sent."}, status=status.HTTP_200_OK)
    except models.CustomUser.DoesNotExist:
        return Response({"error": "This email does not exist."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def reset_password_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = models.CustomUser.objects.get(pk=uid)
        if user.password_reset_token_expires_at < timezone.now():
            return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
        if default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            try:
                utils.validate_passwords(new_password, confirm_password)
                user.set_password(new_password)
                user.save()
                reponse = Response()
                reponse = redirect('home')
                return reponse
            except utils.PasswordValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Le token est invalide ou a expiré."}, status=status.HTTP_400_BAD_REQUEST)
    except (models.CustomUser.DoesNotExist, ValueError, TypeError):
        return Response({"error": "Le lien de réinitialisation est invalide."}, status=status.HTTP_400_BAD_REQUEST)

#**************************************************************************************************************#

@api_view(['GET'])
def logout(request:Request):
    if  request.user.is_anonymous:
            return redirect('home')
    token = request.COOKIES.get('jwt')
    user = request.user
    user.is_online = False
    user.save()
    response = Response({"message": "Déconnecté avec succès"}, status=200)
    response.delete_cookie('jwt')  # Utilisez le token expiré
    return response

#********************************************LOGIN*****************************************************************#

@api_view(['POST', 'GET'])
def login(request: Request):
    # if request.method == "GET":
    #     if request.user.is_anonymous:
    #         return redirect('home')
    #     else :
    #         return redirect('profile')
    serializer = serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')
    user = models.CustomUser.objects.filter(Q(username=username) | Q(email=email)).first()
    if user is None:
        raise AuthenticationFailed('User not found')
    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password')
    token = utils.generate_token(user, True)
    response = Response()
    user.is_online = True
    if user.active_2fa is True:
        user.code_otp, r_code_otp =  utils.generate_random(8)
        user.is_logged_2fa = True
        response = redirect('otp')
        utils.send_code(user.email, r_code_otp, user.username)
    else:
        response = redirect('profile')
    response.set_cookie(key ='jwt', value=token, httponly=True, secure=True)
    user.is_online = True
    user.save()
    return response



@api_view(['GET', 'POST'])
def otp(request: Request):
    if request.user.is_anonymous or request.user.is_logged_2fa is not True:
         return redirect('home')
    if request.method == "POST":
        try:
            serializer = serializers.verify_otp_Serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            response = Response()
            response = redirect('profile')
            token = utils.generate_token(request.user, True)
            response.set_cookie(key ='jwt', value=token, httponly=True, secure=True)
            user = request.user
            user.is_logged_2fa = False
            user.save()
            return response
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=400)
    return Response("message: verified and logged")


#**************************************************************************************************************#



#*************************************PROFILE*********************************************************************#

@api_view(['GET'])
def profile(request:Request):
    if request.user.is_anonymous:
        return redirect('home')
    serializer = serializers.CustomUserProfileSerializer(request.user, context={'request': request})
    return Response({"data": serializer.data, "message": "Profile retrieved successfully"})

#**************************************************************************************************************#

#****************************************Friendship*************************************************************#

@api_view(['POST'])
def send_friend_request(request: Request):

    try:
        user_end = request.user
        friend_name = models.CustomUser.objects.get(username=request.data.get("username_friend"))
        if user_end == friend_name:
            return Response({"detail": "incorrect request"}, status=status.HTTP_404_NOT_FOUND)
        existing_friendship = models.Friendship.objects.filter(
            (Q(user=user_end.id) & Q(friend=friend_name.id)) | (Q(user=friend_name.id) & Q(friend=user_end.id))).first()
        if existing_friendship:
            if not existing_friendship.accepted:
                return Response({"message": "Une demande d'amitié a déjà été envoyée."},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Vous êtes déjà amis."},status=status.HTTP_400_BAD_REQUEST)
        friendship = models.Friendship.objects.create(user=user_end, friend=friend_name)
        return Response( {"message": "Demande d'amitié envoyée avec succès."}, status=status.HTTP_201_CREATED)
    except models.CustomUser.DoesNotExist:
        return Response({"detail": "username_friend not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def accept_friend_request(request: Request):
    if request.user.is_anonymous:
        return redirect('home')
    username_friend = request.data.get("username_friend")
    if not username_friend:
        return Response({"detail": "username_friend is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        to_user = models.CustomUser.objects.get(username=username_friend)
        friendship = models.Friendship.objects.get(user=to_user, friend=request.user)
        if friendship.accepted:
            return Response({"detail": "Friend request has already been accepted."}, status=status.HTTP_400_BAD_REQUEST)
        friendship.accepted = True
        friendship.save()
        return Response({"detail": "Friend request accepted."}, status=status.HTTP_200_OK)
    except models.CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except models.Friendship.DoesNotExist:
        return Response({"detail": "No invitation found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def list_friends(request:Request):
    if request.user.is_anonymous:
        return redirect('home')
    friendships = models.Friendship.objects.filter(Q(user=request.user) | Q(friend=request.user), accepted=True)
    if not friendships:
        return Response({"detail": "No friend found."}, status=status.HTTP_404_NOT_FOUND)
    friends_list = []
    for friendship in friendships:
        if friendship.user == request.user:
            if utils.return_image(friendship.friend.avatar) is True:
                avatar = request.build_absolute_uri(settings.MEDIA_URL + friendship.friend.avatar)
            else :
                avatar = request.build_absolute_uri(settings.MEDIA_URL + 'avatars/default_avatar.png')
            friends_list.append({
                "username": friendship.friend.username,
                "avatar": avatar
            })
        else:
            if utils.return_image(friendship.user.avatar) is True:
                avatar = request.build_absolute_uri(settings.MEDIA_URL + friendship.user.avatar)
            else :
                avatar = request.build_absolute_uri(settings.MEDIA_URL + 'avatars/default_avatar.png')
            friends_list.append({
                "username": friendship.user.username,
                "avatar": avatar
            })
    return Response(friends_list, status=status.HTTP_200_OK)



@api_view(['DELETE'])
def remove_friend(request: Request):
    if request.user.is_anonymous:
        return redirect('home')
    user_end = request.user
    friend_name = request.data.get("username_friend")
    if friend_name is None:
        return Response({"detail": "Please enter 'username_friend'."}, status=status.HTTP_400_BAD_REQUEST)
    friend_user = models.CustomUser.objects.filter(username=friend_name).first()
    if friend_user is None:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    friendship = models.Friendship.objects.filter((Q(user=user_end) & Q(friend=friend_user)) | (Q(user=friend_user) & Q(friend=user_end)) ).first()
    if friendship is None:
        return Response({"detail": "Friendship relationship not found."}, status=status.HTTP_404_NOT_FOUND)
    friendship.delete()
    return Response({"message": "Friend successfully deleted."}, status=status.HTTP_200_OK)



@api_view(['GET'])
def list_requst_friend(request: Request):
    if request.user.is_anonymous:
        return redirect('home')
    user_end = request.user
    list_request_friend =  models.Friendship.objects.filter(Q(friend=request.user), accepted=False)
    if not list_request_friend:
        return Response({"message": "no invitation received"}, status=status.HTTP_200_OK)
    friend_requests = []
    for friendship in list_request_friend:
        if utils.return_image(friendship.user.avatar) is True:
            avatar = request.build_absolute_uri(settings.MEDIA_URL + friendship.user.avatar)
        else :
            avatar = request.build_absolute_uri(settings.MEDIA_URL + 'avatars/default_avatar.png')
        friend_requests.append({
                "username": friendship.user.username,
                "avatar": avatar
            })
    return Response({"requests": friend_requests}, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_friend(request: Request):
    if request.user.is_anonymous:
        return redirect('home')
    user_name = request.GET.get('q')
    if not user_name:
        return Response({"detail": "Enter username"}, status=status.HTTP_404_NOT_FOUND)
    elif request.user.username == user_name:
        return redirect("profile")
    try:
        user_friend = models.CustomUser.objects.get(username=user_name)
    except models.CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    list_data_user = {}
    if utils.return_image(user_friend.avatar) is True:
        avatar = request.build_absolute_uri(settings.MEDIA_URL + user_friend.avatar)
    else :
        avatar = request.build_absolute_uri(settings.MEDIA_URL + 'avatars/default_avatar.png')
    list_data_user["username"] = user_friend.username
    list_data_user["avatar"] = avatar
    status_friendship = "not friend"
    existing_friendship = models.Friendship.objects.filter(Q(user=request.user, friend=user_friend) | Q(user=user_friend, friend=request.user)).first()
    if existing_friendship:
        if existing_friendship.accepted:
            status_friendship = "friend"
        else:
            status_friendship = "already invited"
    list_data_user["status_friendship"] = status_friendship
    return Response({"list_data_user": list_data_user}, status=status.HTTP_200_OK)


#traitre reespnse de rest password et euuer ne autorise google
## handel image foor google familyname

# http://localhost:8000/oauth/login/
# @api_view(['GET'])
# def remove_requst_friend(request: Request):



    # elif existing_friendship = models.Friendship.objects.filter((Q(user=user_friend.id) & Q(friend=request.user.id)))
        # existing_friendship = models.Friendship.objects.filter((Q(user=user_friend.id) & Q(friend=request.user.id)))
        # if not existing_friendship :

    # list_data_user.append(user_friend.avatar)

# @api_view(['GET'])
# def profile_user(request: Request, username):
#     if request.user.is_anonymous:
#         return redirect('home')
#     print(f"DATA =------>>> {request.data}")
#     # user_name = request.GET.get('q')
#     # user = models.CustomUser.objects.filter(username=user_name)
#     # if user:
#         # redirect()
#     return Response({"detail": "User not found. QQ"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def  profile_user(request: Request):
#     if  request.user.is_anonymous:
#         return redirect('home')
#     user_name = request.GET.get('q')
#     user = models.CustomUser.objects.filter(username=user_name)
#     if user:
#         serializer = serializers.UserProfileSerializer(user)
#         return Response({"data": serializer.data, "message": "Profile retrieved successfully"})
#     return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)











#************************************************************************************************************#

# https://www.youtube.com/watch?v=Zo2Uupw2hNg

# http://127.0.0.1:8000/authorize/
# https://www.stagiaires.ma/offres-de-stages-et-premier-emploi-maroc/202895-stage-en-developpement-informatique-backend-developpement-ouled-tayeb/?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic
# LIZAR BUSINESS SERVICES
#https://www.youtube.com/watch?v=ix76SFstT0I&list=RDGMEM6ijAnFTG9nX1G-kbWBUCJA&index=5


# @api_view(['POST'])
# def accept_friend_request(request:Request):
#     if request.user.is_anonymous:
#         return redirect('home')
#     try:
#         to_user =  models.CustomUser.objects.get(username=request.data.get("username_friend"))
#         print(f"To user ===== >>>> {to_user}")
#         friendship = models.Friendship.objects.get(user=to_user.id, friend=request.user.id)
#         if not friendship:
#             return Response({"detail": "no invitation"}, status=status.HTTP_400_BAD_REQUEST)
#         if friendship.accepted:
#             return Response({"detail": "Friend request has already been accepted."}, status=status.HTTP_400_BAD_REQUEST)
#         friendship.accepted = True
#         friendship.save()
#         return Response({"detail": "Friend request accepted."}, status=status.HTTP_200_OK)
#     except (models.Friendship.DoesNotExistmodels, models.CustomUser.DoesNotExist) as e:
#         return Response({"detail": "{e}"}, status=status.HTTP_404_NOT_FOUND)
