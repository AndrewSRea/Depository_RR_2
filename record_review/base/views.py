from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count, FloatField, Q, Sum
from django.db.models.functions import Cast, Round
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Album, Review, User
from .forms import AlbumForm, UserForm, MyUserCreationForm


ALBUMS_PER_PAGE = 5


def login_page(request):
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
			messages.error(request, 'Username and/or password does not exist')

	context = {'page': page}
	return render(request, 'base/login_register.html', context)


def logout_user(request):
	logout(request)
	return redirect('home')


def register_page(request):
	form = MyUserCreationForm()

	if request.method == 'POST':
		form = MyUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = form.cleaned_data.get('username')
			user.save()
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, 'An error occurred during registration.')

	return render(request, 'base/login_register.html', {'form': form})


# for the home page
def home(request):
	# search bar
	q = request.GET.get('q') if request.GET.get('q') != None else ''

	albums = Album.objects.filter(Q(artist__icontains=q) | Q(title__icontains=q))

	# ** Pagination **
	# paginator = Paginator(albums, 5)

	# page_number = request.GET.get("page")
	# page_obj = paginator.get_page(page_number) -- don't forget `page_obj` in the `context` below!

	# ** Coding with Mitch Paginator **
	page = request.GET.get("page", 1)
	albums_paginator = Paginator(albums, ALBUMS_PER_PAGE)

	try:
		albums = albums_paginator.page(page)
	except PageNotAnInteger:
		albums = albums_paginator.page(ALBUMS_PER_PAGE)
	except EmptyPage:
		albums = albums.paginator.page(albums_paginator.num_pages)

	# the "Highest Rated" list (Fingers crossed!)
	ratings_list = Album.objects.annotate(
		ratings_avg=Round(Cast((Sum('rating', distinct=True) + Sum('review__rating')), output_field=FloatField()) 
			/ (Count('review__rating') + 1), precision=2)
	).order_by('-ratings_avg')[0:5]

	# "Reviews" count -- change this to a `Count()` function?
	num_of_albums = Album.objects.all()
	album_count = num_of_albums.count()

	# "Recent Activity" -- you can limit this with `[0:10]`
	album_reviews = Review.objects.all()[0:5]

	context = {
		'albums': albums, 
		'ratings_list': ratings_list, 
		'album_count': album_count, 
		'album_reviews': album_reviews
		# 'page_obj': page_obj
	}
	return render(request, 'base/home.html', context)


# for a specific album page
def album(request, pk):
	album = Album.objects.get(id=pk)
	reviews = album.review_set.all()

	if request.method == 'POST':
		review = Review.objects.create(
			reviewer=request.user,
			album=album,
			comment=request.POST.get('comment'),
			rating=request.POST.get('rating')
		)
		return redirect('album', pk=album.id)

	ratings_list = Album.objects.annotate(
		ratings_avg=Round(Cast((Sum('rating', distinct=True) + Sum('review__rating')), output_field=FloatField()) 
			/ (Count('review__rating') + 1), precision=2)
	).order_by('-ratings_avg')[0:5]

	album_reviews = Review.objects.all()

	context = {
		'album': album, 
		'reviews': reviews, 
		'ratings_list': ratings_list, 
		'album_reviews': album_reviews
	}
	return render(request, 'base/album.html', context) 


def user_profile(request, pk):
	user = User.objects.get(id=pk)
	albums = user.album_set.all()

	# *** CHANGE THESE TWO PARAMETERS IF YOU WANT TO SOLELY DISPLAY USER'S REVIEWS AND RATINGS ***
	# the "Highest Rated" list
	ratings_list = Album.objects.annotate(
		ratings_avg=Round(Cast((Sum('rating', distinct=True) + Sum('review__rating')), output_field=FloatField()) 
			/ (Count('review__rating') + 1), precision=2)
	).order_by('-ratings_avg')[0:5]

	# "Recent Activity" -- you can limit this with `[0:10]`
	album_reviews = Review.objects.all()
	# **********************************

	context = {
		'user': user, 
		'albums': albums, 
		'ratings_list': ratings_list,
		'album_reviews': album_reviews
	}
	return render(request, 'base/profile.html', context)


# the form for creating an album review
@login_required(login_url='login')
def create_album(request):
	form = AlbumForm()

	if request.method == 'POST':
		form = AlbumForm(request.POST, request.FILES)
		if form.is_valid():
			album = form.save(commit=False)
			album.creator = request.user
			form.save()
			return redirect('home')

	context = {'form': form}
	return render(request, 'base/album_form.html', context)


@login_required(login_url='login')
def update_album(request, pk):
	album = Album.objects.get(id=pk)
	form = AlbumForm(instance=album)

	if request.user != album.creator:
		return HttpResponse('You do not have permission to edit this album.')

	if request.method == 'POST':
		form = AlbumForm(request.POST, request.FILES, instance=album)
		if form.is_valid():
			form.save()
			return redirect('home')

	context = {'form': form, 'album': album}
	return render(request, 'base/album_form.html', context)


@login_required(login_url='login')
def delete_album(request, pk):
	album = Album.objects.get(id=pk)

	if request.user != album.creator:
		return HttpResponse('You do not have permission to delete this album.')

	if request.method == 'POST':
		album.delete()
		return redirect('home')
	return render(request, 'base/delete.html', {'obj': album})


@login_required(login_url='login')
def delete_review(request, pk):
	review = Review.objects.get(id=pk)

	if request.user != review.reviewer:
		return HttpResponse('You do not have permission to delete this review.')

	if request.method == 'POST':
		review.delete()
		return redirect('home')
	return render(request, 'base/delete.html', {'obj': review})


@login_required(login_url='login')
def update_profile(request):
	user = request.user
	form = UserForm(instance=user)
	
	if request.method == 'POST':
		form = UserForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect('user-profile', pk=user.id)

	return render(request, 'base/update_profile.html', {'form': form})


def highest_rated(request):
	albums = Album.objects.all()
	reviews = Review.objects.all()

	ratings_list = Album.objects.annotate(
		ratings_avg=Round(Cast((Sum('rating', distinct=True) + Sum('review__rating')), output_field=FloatField()) 
			/ (Count('review__rating') + 1), precision=2)
	).order_by('-ratings_avg')[0:10]

	context = {'albums': albums, 'reviews': reviews, 'ratings_list': ratings_list}

	return render(request, 'base/highest_rated.html', context)


def recent_activity(request):
	album_reviews = Review.objects.all()[0:10]

	return render(request, 'base/activity.html', {'album_reviews': album_reviews})