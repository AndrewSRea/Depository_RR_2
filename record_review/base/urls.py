from django.urls import path 
from . import views


urlpatterns = [
	path('login/', views.login_page, name="login"),
	path('logout/', views.logout_user, name="logout"),
	path('register/', views.register_page, name="register"),

	path('', views.home, name="home"),
	path('album/<str:pk>/', views.album, name="album"),
	path('profile/<str:pk>/', views.user_profile, name="user-profile"),

	path('create-album/', views.create_album, name="create-album"),
	path('update-album/<str:pk>/', views.update_album, name="update-album"),
	path('delete-album/<str:pk>/', views.delete_album, name="delete-album"),
	path('delete-review/<str:pk>/', views.delete_review, name="delete-review"),

	path('update-profile/', views.update_profile, name="update-profile"),

	path('highest-rated/', views.highest_rated, name="highest-rated"),
	path('activity/', views.recent_activity, name="activity"),
]