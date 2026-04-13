# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from crispy_forms.helper import FormHelper

class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(required=False)
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Crispy helper
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.attrs = {'autocomplete': 'off'}
        

        for field_name, field in self.fields.items():            
            field.widget.attrs.update({
                'class': 'form__input',
                'placeholder': ' ',
                
            })
        
        # Optional: remove default password help text
        # self.fields['password2'].help_text = None