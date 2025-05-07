# users/backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    This backend authenticates with either username or email
    """
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        # Try to authenticate by email if provided explicitly
        if email:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        
        # Try with username parameter as either username or email
        if username:
            # Check if the username value could be an email
            try:
                # First try exact username match
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                try:
                    # Then try with username as email
                    user = User.objects.get(email=username)
                    if user.check_password(password):
                        return user
                except User.DoesNotExist:
                    return None
                
        return None