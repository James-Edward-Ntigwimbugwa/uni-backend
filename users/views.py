from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChangePasswordSerializer, ProfilePhotoSerializer, RegisterSerializer , MessageSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Message 

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "error": False,
                "message": "Registered successfully",
                "data": {
                    "id": user.id,
                    "username": user.username
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "error": True,
            "message": "Registration failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        # Support both email and username for login
        identifier = request.data.get('email') or request.data.get('username')
        password = request.data.get('password')
        
        if not identifier or not password:
            return Response(
                {'error': 'Please provide both email/username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to authenticate with email
        user = authenticate(email=identifier, password=password)
        
        # If email authentication fails, try with username
        if user is None:
            user = authenticate(username=identifier, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'message': 'Login successful',
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'access_token': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_200_OK
        )
        


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            
            # Debug information
            print(f"Checking password for user====>: {self.object.email}")
            print(f"Old password provided====>: {old_password}")
            
            if not self.object.check_password(old_password):
                return Response(
                    {"message": "Wrong password."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            self.object.set_password(serializer.validated_data.get("new_password"))
            self.object.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfilePhotoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfilePhotoSerializer(user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile photo updated successfully",
                "profile_photo": request.build_absolute_uri(user.profile_photo.url) if user.profile_photo else None
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # Both staff and students can send messages
            message = serializer.save(sender=request.user)
            return Response({
                "error": False,
                "message": "Message sent successfully",
                "data": {
                    "id": message.id,
                    "subject": message.subject,
                    "sent_at": message.sent_at
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "error": True,
            "message": "Message sending failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
class MessageListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            messages = Message.objects.all().order_by('-sent_at')
            serializer = MessageSerializer(messages, many=True)
            return Response({
                "error": False,
                "message": "Messages retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": True,
                "message": "Failed to retrieve messages",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)