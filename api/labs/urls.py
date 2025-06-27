from django.urls import path
from . import views

urlpatterns = [
    path('labs', views.get_labs),
    path('add-or-edit-lab', views.add_or_edit_lab_view),
    path('labs/<str:lab_id>/', views.update_lab_view),
    path('delete-lab/<str:lab_id>', views.delete_lab_view),
    path('bulk-delete-labs', views.bulk_delete_labs_view),
]
