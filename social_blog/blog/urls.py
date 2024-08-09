from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostsListView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostsDetailView.as_view(),
         name='post_detail'),
    path('category/<slug:category_slug>/', views.CategoryListView.as_view(),
         name='category_posts'),
    path('profile/<str:username>/', views.ProfileView, name='profile'),
    path('edit_profile/', views.ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('posts/create/', views.PostsCreateView.as_view(),
         name='create_post'),
    path('posts/<post_id>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<post_id>/delete/', views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<post_id>/comment/', views.CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<post_id>/edit_comment/<comment_id>/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<post_id>/delete_comment/<comment_id>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
]
