from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = User._meta.get_field (
        "email"
    ).formfield(required=True)

    class meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
