from django import forms
from .models import Profiles, Banners


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Profiles
        fields = ['user_profile','image']

class BannerForm(forms.ModelForm):
    """Form for the banner model"""
    class Meta:
        model = Banners
        fields = ['user_profile','banner']