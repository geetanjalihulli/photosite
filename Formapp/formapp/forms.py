import os
from django import forms
from settings import MEDIA_ROOT


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=200)
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label = 'Enter Password' )
    password2 = forms.CharField(widget=forms.PasswordInput, label = 'Re-Enter Password')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)


class UploadImageForm(forms.Form):
    image = forms.ImageField()
    caption = forms.CharField(max_length=200)

    def handle_uploaded_file(self, image, name, album_name):
        exist_path = os.path.join(MEDIA_ROOT, name)
        if not os.path.exists(exist_path):
            os.mkdir(exist_path)
        album_path = os.path.join(exist_path, album_name)
        if not os.path.exists(album_path):
            os.mkdir(album_path)
        destination = open(album_path +'/'+ image.name, 'wb+')
        for chunk in image.chunks():
            destination.write(chunk)
        destination.close()

class PhotoAlbumForm(forms.Form):
    album_name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=2000)

