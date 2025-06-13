from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_conversations_view),
    path('add', views.add_conversation_view),
    path('add/<str:convo_id>', views.get_conversation_view),
    path('delete/<str:convo_id>', views.delete_conversation_view),
    path('bulk-delete', views.bulk_delete_conversations_view),
]
