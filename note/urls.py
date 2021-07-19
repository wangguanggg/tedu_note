from django.urls import path
from . import views
urlpatterns = [
    path('add', views.add_note),
    path('all', views.all_view),
    path('delete', views.delete_view),
    path('update', views.update_view),
    path('download', views.download_view),
    path('downpage', views.downpage_view)
]