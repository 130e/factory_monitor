from django.contrib.auth.forms import UserCreationForm
from .models import User

# we use our model
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email") # manually include email