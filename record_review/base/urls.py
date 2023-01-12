from django.urls import path 
from . import views

urlpatterns = [
  path('login/', views.loginPage, name="login"),
  path('logout/', views.logoutUser, name="logout"),
  path('register/', views.registerPage, name="register"),

  path('', views.home, name="home"),
  path('review/<str:pk>/', views.review, name="review"),
  path('profile/<str:pk>', views.userProfile, name="user-profile"),

  path('create-review/', views.createReview, name="create-review"),
  path('update-review/<str:pk>/', views.updateReview, name="update-review"),
  path('delete-review/<str:pk>/', views.deleteReview, name="delete-review"),
  path('delete-added-review/<str:pk>/', views.deleteAddedReview, name="delete-added-review")
]