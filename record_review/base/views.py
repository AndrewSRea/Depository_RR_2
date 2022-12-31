from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Review, AddedReview
from .forms import ReviewForm


# reviews = [
#   {'id': 1, 'album': 'Sleeps With Angels', 'artist': 'Neil Young'},
#   {'id': 2, 'album': 'Vitalogy', 'artist': 'Pearl Jam'},
#   {'id': 3, 'album': 'Nevermind', 'artist': 'Nirvana'},
# ]


def loginPage(request):
  page = 'login'

  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')


    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, 'User does not exist')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username or password does not exist')

  context = {'page': page}
  return render(request, 'base/login_register.html', context)


def logoutUser(request):
  logout(request)
  return redirect('home')


def registerPage(request):
  form = UserCreationForm()

  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = form.cleaned_data.get('username')
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'An error occurred during registration')

  return render(request, 'base/login_register.html', {'form': form})


# Home page
def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''

  reviews = Review.objects.filter(Q(artist__icontains=q) | Q(album__icontains=q))

  added_reviews = AddedReview.objects.all()

  # if you want to add a header: <h5>{{reviews_count}} Reviews Created</h5>
  # pass `'reviews_count': reviews_count` in the `context` below
  # reviews_count = reviews.count()

  highest_list = Review.objects.all().order_by('-rating')
  lowest_list = Review.objects.all().order_by('rating')
  a_z_artist_list = Review.objects.all().order_by('artist')
  #a_z_album_list =

  context = {
    'reviews': reviews, 
    'highest_list': highest_list, 
    'lowest_list': lowest_list, 
    'a_z_artist_list': a_z_artist_list,
    'added_reviews': added_reviews
  } # maybe have to create a `list` function?

  return render(request, 'base/home.html', context)


# Individual review page
def review(request, pk):
  review = Review.objects.get(id=pk)
  added_reviews = review.addedreview_set.all()

  if request.method == 'POST':
    added_review = AddedReview.objects.create(
      user=request.user,
      review=review,
      body=request.POST.get('body')
    )
    return redirect('review', pk=review.id)

  context = {'review': review, 'added_reviews': added_reviews}
  return render(request, 'base/review.html', context)


# Create a Review form
@login_required(login_url='login')
def createReview(request):
  form = ReviewForm()
  if request.method == 'POST':
    form = ReviewForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/review_form.html', context)


# Not sure if I need this but it might be necessary if a user thinks he/she messed up their
# initial review
@login_required(login_url='login')
def updateReview(request, pk):
  review = Review.objects.get(id=pk)
  form = ReviewForm(instance=review)

  if request.user != review.author:
    return HttpResponse('You are not allowed here!')

  if request.method == 'POST':
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid:
      form.save()
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/review_form.html', context)


# I think the instructor will set this up so you'll only be able to see the "delete" button on their
# own reviews if they're logged in
@login_required(login_url='login')
def deleteReview(request, pk):
  review = Review.objects.get(id=pk)

  if request.user != review.author:
    return HttpResponse('You are not allowed here!')

  if request.method == 'POST':
    review.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj': review})


@login_required(login_url='login')
def deleteAddedReview(request, pk):
  added_review = AddedReview.objects.get(id=pk)

  if request.user != added_review.user:
    return HttpResponse('You are not allowed here!')

  if request.method == 'POST':
    added_review.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj': added_review})