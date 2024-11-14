# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart

# # def send_email(to_email, code):
# #     from_email = 'maaloum.yassine@gmail.com'
# #     password = 'xayc rbdp axbd yfpk'  # Utilise le mot de passe d'application ici

# #     subject = 'Votre code 2FA'
    
# #     message = f'Votre code de vérification est : {code}'

# #     msg = MIMEMultipart()
# #     msg['From'] = from_email
# #     msg['To'] = to_email
# #     msg['Subject'] = subject
# #     msg.attach(MIMEText(message, 'plain'))

# #     try:
# #         with smtplib.SMTP('smtp.gmail.com', 587) as server:
# #             server.starttls()
# #             server.login(from_email, password)  # Utilise le mot de passe d'application
# #             server.sendmail(from_email, to_email, msg.as_string())
# #             print('Email envoyé avec succès.')
# #     except Exception as e:
# #         print(f'Erreur lors de l\'envoi de l\'email : {e}')







# # @api_view(['POST', 'GET'])
# # def signup(request:Request):
# #     serializer = serializers.CustomUserRegisterSerializer(data=request.data)
# #     if serializer.is_valid():
# #         if not verify_email(request.data.get('email')):
# #             return Response({"error": "Cet email est invalide."}, status=status.HTTP_400_BAD_REQUEST) 
# #         user_data = {
# #         'username': request.data.get('username'),
# #         'email': request.data.get('email'),
# #         'first_name':request.data.get('first_name'),
# #         'last_name':request.data.get('last_name'),
# #         'password': request.data.get('password'),
# #         'verification_code':generate_random(6) 
# #         }
# #         temporary_users[user_data['username']] = user_data
# #         send_email(user_data['email'], user_data['verification_code'])
# #         return Response({
# #         "message": "Un code de vérification a été envoyé à votre adresse email.",
# #         "redirect_url": "/enter-verification-code"
# #         }, status=status.HTTP_201_CREATED)
    
# #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # # @api_view(['POST'])
# # # def verify_code(request):
# # #     username = request.data.get('username')
# # #     code = request.data.get('code')
# # #     if username in temporary_users:
# # #         user_data = temporary_users[username]
# # #         if user_data['verification_code'] == code:
# # #             CustomUser.objects.create_user(
# # #                 username=user_data['username'],
# # #                 email=user_data['email'],
# # #                 first_name=user_data['first_name'],
# # #                 last_name=user_data['last_name'],
# # #                 password=user_data['password']
# # #             )
# # #             del temporary_users[username]
# # #             return Response({"message": "Votre compte a été vérifié avec succès."}, status=status.HTTP_200_OK)
# # #         else:
# # #             return Response({"error": "Code de vérification invalide."}, status=status.HTTP_400_BAD_REQUEST)
# # #     else:
# # #         return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)


# # # @api_view(['POST', 'GET'])
# # # def login(request:Request):
# # #     if request.method == "GET":
# # #         if request.user.is_anonymous:
# # #             return redirect('home')
# # #         else :
# # #             return redirect('profile')
# # #     elif request.user.is_anonymous:
# # #         serializer = serializers.LoginSerializer(data=request.data)
# # #         serializer.is_valid(raise_exception=True)  
# # #         username = serializer.validated_data.get('username')
# # #         email = serializer.validated_data.get('email')
# # #         password = serializer.validated_data.get('password')
# # #         user = models.CustomUser.objects.filter(Q(username=username) | Q(email=email)).first()
# # #         if user is None:
# # #             raise AuthenticationFailed('User not found')
# # #         if not user.check_password(password):
# # #             raise AuthenticationFailed('Incorrect password')
# # #         request.user = user
# # #         token = generate_token(user)
# # #         response = Response()
# # #         response = redirect('profile') 
# # #         response.set_cookie(key ='jwt', value=token, httponly=True, secure=True)
# # #         response.data = {
# # #             'jwt': token
# # #         }
# # #         return response 
# # #     return redirect('profile')
    


#    # if request.method == "GET":
#     #     if request.user.is_anonymous:
#     #        return redirect('home')
#     #     else :
#     #         return redirect('profile')



# @api_view(['PUT', 'GET'])
# def update(request:Request):
#     user = request.user 
#     if request.user.is_anonymous:
#         return redirect('home')
#     user = request.user 
#     new_email = request.data.get("email")
#     serializer = serializers.CustomUserUpdateSerializer(user, data=request.data, partial=True) 
#     if serializer.is_valid():
#         validated_data = serializer.validated_data
#         if new_email and new_email != user.email:
#             password = validated_data.pop('password')
#             validated_data.pop('confirm_password')  
#             hashed_password = make_password(password)  
#             validated_data['password'] = hashed_password
#             fake_user = CustomUser(**validated_data)
#             token = default_token_generator.make_token(fake_user)
#             uid = urlsafe_base64_encode(force_bytes(fake_user.username))  
#             user_key = f"user:{validated_data['username']}"
#             redis_client.set(user_key, json.dumps(validated_data), ex=60)  
#             verification_link = f"http://localhost:8000/verify_account/{uid}/{token}/"
#             html_message = render_to_string('verfycompte_template.html', {
#                 'reset_link': verification_link,
#             })
#             send_email(validated_data['email'], html_message, False)
        
#         # serializer.save()  # Sauvegarde les nouvelles données de l'utilisateur
#         # return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # if new_email and new_email != user.email:
#     # else :

   