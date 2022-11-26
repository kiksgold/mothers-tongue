from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete_post'),
]
