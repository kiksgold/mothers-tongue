from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.category, name='category'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
