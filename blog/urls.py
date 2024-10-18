from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),  # Blog list view
    path('search/', views.blog_search, name='blog_search'),  # Full-text search
    path('search/trigram/', views.blog_search_trigram, name='blog_search_trigram'),  # Trigram search
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),  # Blog detail view
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),  # Add comment to a blog
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),  # Like a comment
    path('comment/<int:comment_id>/dislike/', views.dislike_comment, name='dislike_comment'),  # Dislike a comment
    path('<slug:slug>/share/', views.share_blog, name='share_blog'),  # Share blog via email
]
