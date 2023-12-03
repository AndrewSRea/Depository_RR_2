from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Album, User


class MyUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2']


class AlbumForm(ModelForm):
  class Meta:
    model = Album
    fields = '__all__'
    exclude = ['creator', 'created']
    labels = {
      'artist': _('Artist or Band Name'),
      'title': _('Album Title'),
      'image': _('Album Image'),
      'rating': _('Rating (1-10)'),
      'comment': _('Your Review'),
    }

# when you add an image to the form, delete `exclude = []`, then add `'creator', 'image', 'created'` to `exclude`
# See your notes in Github

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['image', 'username', 'bio']
    labels = {
      'image': _('Profile Photo'),
    }