from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_reg_page),
    path('create_user', views.create_user),
    path('login',views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard_page),
    path('shows/add', views.add_show_page),
    path('shows/create', views.create_show),
    path('shows/<int:show_id>/edit', views.edit_show_page),
    path('shows/<int:show_id>/update', views.update_show),
    path('shows/<int:show_id>', views.view_show_page),
    path('shows/<int:show_id>/delete', views.delete_show),
    path('shows/<int:show_id>/add-to-user', views.add_show_to_user),
    path('shows/<int:show_id>/remove-from-user', views.remove_show_from_user),
    path('shows/<int:show_id>/done', views.done_show)
]