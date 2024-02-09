from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    """This form will extend the fields of the standard Django Form"""

    # Extend the base User Creation Form with those fields
    email = forms.EmailField(
        label="Email",
        max_length=254
    )
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        # Change password2 (confirm password) label from UserCreationForm
        self.fields["password2"].label = "Confirm Password"