from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm
from .models import Review, AddedReview
from .forms import ReviewForm, UserForm


# reviews = [
#   {'id': 1, 'artist': 'Neil Young', 'album': 'Sleeps with Angels'},
#   {'id': 2, 'artist': 'Pearl Jam', 'album': 'Vitalogy'},
#   {'id': 3, 'artist': 'Nirvana', 'album': 'Nevermind'},
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


# def average(request, pk):
#   added_ratings_sum = Review.objects.get(id=pk).aggregate(Sum('addedreview__rating'))

#   print(added_ratings_sum)

#   for i in added_ratings_sum.values():
#     a_r_sum = i

#   orig_ratings_sum = Review.objects.get(id=pk).aggregate(Sum('rating'))

#   for j in orig_ratings_sum.values():
#     r_sum = j

#   total_sum = a_r_sum + r_sum

#   ratings_count = Review.objects.get(id=pk).addedreview_set.count() + 1

#   ratings_avg = total_sum / ratings_count

#   return render(request, 'base/home.html', {'ratings_avg': ratings_avg})


def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''

  reviews = Review.objects.filter(Q(artist__icontains=q) | Q(album__icontains=q))
  review_count = reviews.count()
  added_reviews = AddedReview.objects.all()

  highest_list = Review.objects.all().order_by('-rating')[0:5]

  # Instructor alluded to creating `if` statements here in a view in order to render certain data
  # This would help with your "Highest Rated" dropdown -- so you will have to make a `list` view
  context = {
    'reviews': reviews, 
    'highest_list': highest_list, 
    'review_count': review_count, 
    'added_reviews': added_reviews
  }
  return render(request, 'base/home.html', context)


def review(request, pk):
  review = Review.objects.get(id=pk)
  added_reviews = review.addedreview_set.all()

  # added_ratings_sum = Review.objects.get(id=pk).aggregate(Sum('addedreview__rating'))

  # for i in added_ratings_sum.values():
  #   a_r_sum = i

  # orig_ratings_sum = Review.objects.get(id=pk).aggregate(Sum('rating'))

  # for j in orig_ratings_sum.values():
  #   r_sum = j

  # total_sum = a_r_sum + r_sum

  # ratings_count = Review.objects.get(id=pk).addedreview_set.count() + 1

  # ratings_avg = total_sum / ratings_count

  # Functionality for `rating` not working. Will have to figure out how to make that work.
  if request.method == 'POST':
    added_review_form = AddedReview.objects.create(
      user=request.user,
      review=review,
      body=request.POST.get('body'),
      rating=request.POST.get('rating')
    )
    return redirect('review', pk=review.id)

  context = {
    'review': review, 
    'added_reviews': added_reviews
  }
  return render(request, 'base/review.html', context)


def userProfile(request, pk):
  user = User.objects.get(id=pk)
  reviews = user.review_set.all()
  added_reviews = user.addedreview_set.all()
  highest_list = Review.objects.all().order_by('-rating')
  context = {
    'user': user, 'reviews': reviews, 'added_reviews': added_reviews, 'highest_list': highest_list
  }
  return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createReview(request):
  form = ReviewForm()

  if request.method == 'POST':
    form = ReviewForm(request.POST)
    if form.is_valid():
      review = form.save(commit=False)
      review.author = request.user
      review.save()
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/review_form.html', context)


@login_required(login_url='login')
def updateReview(request, pk):
  review = Review.objects.get(id=pk)
  form = ReviewForm(instance=review)

  if request.user != review.author:
    return HttpResponse('You are not allowed here!')

  if request.method == 'POST':
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
      form.save()
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/review_form.html', context)


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


@login_required(login_url='login')
def updateProfile(request):
  user = request.user
  form = UserForm(instance=user)

  if request.method == 'POST':
    form = UserForm(request.POST, instance=user)
    if form.is_valid():
      form.save()
      return redirect('user-profile', pk=user.id)

  return render(request, 'base/update_profile.html', {'form': form})