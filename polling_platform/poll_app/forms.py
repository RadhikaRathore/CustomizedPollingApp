from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ValidationError
from django.db import transaction

from poll_app.models import User, Poll, EmailId, Choice


class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.save()
        return user


class EmailForm(forms.ModelForm):

    class Meta:
        model = EmailId
        fields = ('email_id', 'username',)


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('choice_text',)
