from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup),
    path('signin', views.login),
    path('logout/', views.logout),
    path('users', views.get_users),
    path('users/<str:user_id>/', views.update_user_view),
    path('delete-user/<str:user_id>', views.delete_user_view),
    path('bulk-delete-users', views.bulk_delete_users_view),
]
