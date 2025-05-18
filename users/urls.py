from django.urls import path
from users.views import (ProfilePhotoView, RegisterView , LoginView , ChangePasswordView, MessageView , MessageListView)

urlpatterns = [
    path('register/' , RegisterView.as_view(), name="register" ),
    path('login/' , LoginView.as_view() , name='login'),
    path('change-password/' ,ChangePasswordView.as_view(), name='change-password'),
    path('profile-photo/' , ProfilePhotoView.as_view(), name='profile-photo'),
    path('send-message/' , MessageView.as_view(), name='send-message' ),
    path("messages/", MessageListView.as_view(), name="message-list")
]
