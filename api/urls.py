from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.get_routes),
    path('posts/', views.get_posts),
    path('posts/<str:pk>/', views.get_post),
    path('posts/<str:pk>/vote/', views.post_vote),

    path('remove-tag/', views.remove_tag)
]
