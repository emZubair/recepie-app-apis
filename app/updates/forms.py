from django import forms
from django.db import models
from django.forms import fields
from .models import UpdateModel


class UpdateModelForm(forms.ModelForm):
    class Meta:
        model = UpdateModel

        fields = [
            'user', 'content', 'image'
        ]

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        content = data.get('content', None)
        image = data.get('image', None)
        if content == '':
            content = None

        if content is None and image is None:
            raise forms.ValidationError('Image or Content is required')
        return super().clean(*args, **kwargs)
