from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
  artist = models.CharField(max_length=100)
  album = models.CharField(max_length=200)
  rating = models.IntegerField(
    validators=[MinValueValidator(0), MaxValueValidator(10)],
    default=10,
  )
  # change the name of `content` with `verbose` for the future form?
  content = models.TextField(null=True, blank=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(default=timezone.now) # date_posted
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  # image =

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return '%s - %s' % (self.artist, self.album)


class AddedReview(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  review = models.ForeignKey(Review, on_delete=models.CASCADE)
  rating = models.IntegerField(default=10)
  # again, change the name of `body` with `verbose` for the future form?
  body = models.TextField()
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(default=timezone.now) # date_posted

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return self.body[0:50]
