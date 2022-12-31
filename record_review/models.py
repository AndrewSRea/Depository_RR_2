from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Review(models.Model):
  artist = models.CharField(max_length=100)
  album = models.CharField(max_length=200)
  rating = models.IntegerField(default=10)
  content = models.TextField(null=True, blank=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(default=timezone.now) # date_posted
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  # image =

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return '%s - %s' % (self.artist, self.album)


# REMEMBER! THIS IS A BREAKABLE PROJECT! Nothing here is written in stone.

# Just learned that any model relating to another model needs to be placed above the model to which it relates.
# i.e. in the instructor's example, he has a `Topic` model, and `topic` is a field in his `Room` model.
# Therefore, he has his `Topic` model above his `Room` model.


class AddedReview(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  review = models.ForeignKey(Review, on_delete=models.CASCADE) # CASCADE will delete all additional reviews in an initial review when the initial review is deleted
  rating = models.IntegerField(default=10)
  body = models.TextField()
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(default=timezone.now) # date_posted

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return self.body[0:50] # This part can show in the right column when a user is logged in to show them recent reviews on their own reviews
