from django.urls import path, include # type: ignore

urlpatterns = [
    path('admin/', include('api.users.urls')),
    path('admin/', include('api.docs.urls')),
    path('admin/', include('api.labs.urls')),
    path('admin/', include('api.messages.urls')),
    path('conversations/', include('api.conversations.urls')),
]
