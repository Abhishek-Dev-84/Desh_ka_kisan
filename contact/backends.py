from django.contrib.auth.backends import BaseBackend
from contact.models import MyUser

class MyUserAuthBackend(BaseBackend):
    def authenticate(self,request,username = None, password = None,**kwargs):
        print("DEBUG: custom authenticate method called")
        try:
            user = MyUser.objects.get(username=username)
            print(f"DEBUG: Found user:{user}")
            if user.check_password(password):
                print("DEBUG: password matched")
                return user
            else:
                print("DEBUG: password mis-matched")
        except MyUser.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None