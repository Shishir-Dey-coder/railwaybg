from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['img']
        widgets = {
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

