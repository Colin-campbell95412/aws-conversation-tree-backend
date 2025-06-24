from django.urls import path
from . import views

urlpatterns = [
    path('messages', views.get_messages),
    path('add-or-edit-message', views.add_or_edit_message_view),
    path('messages/<str:message_id>/', views.update_message_view),  
    path('delete-message/<str:message_id>', views.delete_message_view),
    path('bulk-delete-messages', views.bulk_delete_messages_view),
]