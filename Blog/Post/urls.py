from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('add',views.add,name='add-post'),
    path('details/<slug:slug>',views.detail,name='post_detail'),
    path('edit/<slug:slug>',views.edit,name='edit'),
    path('delete/<slug:slug>',views.delete_post,name='post_delete'),
    path('status/<slug:slug>',views.change_status,name='change_status'),
]