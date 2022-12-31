from django.forms import ModelForm
from .models import Review 


class ReviewForm(ModelForm):
  class Meta:
    model = Review 
    fields = '__all__'


# ^^ When you want to include the 'rating', delete `exclude = ...` and replace it with
# `fields = '__all__'`, save the code, then replace `fields = ...` with `exclude = ...`
# again.


# Hmmm...replace "Content" with "Review"? ("Content" is not very descriptive for a User
# when looking at the Review Form.) (Can I put "review" as field inside the "Review" model?)