from django.urls import path
from . import views

urlpatterns = [
    path('docs', views.get_docs),
    path('add-or-edit-doc', views.add_or_edit_doc_view),
    path('docs/<str:doc_id>/', views.update_doc_view),
    path('delete-doc/<str:doc_id>', views.delete_doc_view),
    path('bulk-delete-docs', views.bulk_delete_docs_view),
]
