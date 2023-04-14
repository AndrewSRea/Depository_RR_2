from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Review
from django.contrib.auth.models import User


class ReviewForm(ModelForm):
  class Meta:
    model = Review 
    fields = '__all__'
    exclude = ['created', 'author']
    labels = {
      'rating': _('Rating (0-10)'),
      'content': _('Your review'),
    }


# RE: the `image` field: "...files that are uploaded using a form need to be handled
# differently (they can be retrieved from `request.FILES`, rather than `request.POST).
# For details of how to handle file uploads with your form, see 'Binding uploaded files
# to a form': https://docs.djangoproject.com/en/4.1/ref/forms/api/#binding-uploaded-files-to-a-form"

# ^^ When you want to include the 'rating', delete `exclude = ...` and replace it with
# `fields = '__all__'`, save the code, then replace `fields = ...` with `exclude = ...`
# again.


# Hmmm...replace "Content" with "Review"? ("Content" is not very descriptive for a User
# when looking at the Review Form.) (Can I put "review" as field inside the "Review" model?)
# ^^^ I believe this can be changed with `verbose_name`.

# See the Django documentation: 
# https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/#selecting-the-fields-to-use

# Buy into Dennis Ivy's full Django course to learn more about form customization?
# https://dennisivy.teachable.com/p/django-beginners-course/?product_id=3222835&coupon_code=BRAD


class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['username']