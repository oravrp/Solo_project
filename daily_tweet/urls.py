from django.urls import path     
from . import views
urlpatterns = [
    path('wel', views.index1),
    path('', views.index),
    path('create_user', views.create_user),
    path('success', views.success),  
    path('login', views.login),
    path('log_out', views.log_out),
    path('process_message', views.post_mess),
    path('add_comment/<int:id>', views.post_comment),
    path('edit_profile/<int:id>', views.edit_profile),
    path('update/<int:id>', views.update),
    path('user_profile/<int:id>', views.profile),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment)
]