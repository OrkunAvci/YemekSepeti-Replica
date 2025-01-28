from django.urls import path
from . import views

app_name = 'master'

urlpatterns = [
    # User-related views
    path('', views.index, name='index'),  # List stores
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Store-related views
    path('store/<int:store_id>/', views.store, name='store'),


    # Manager-related views (single store per manager)
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/add-item/', views.manager_add_item, name='manager_add_item'),
    path('manager/edit-item/<int:item_id>/', views.manager_edit_item, name='manager_edit_item'),
    path('manager/delete-item/<int:item_id>/', views.manager_delete_item, name='manager_delete_item'),


    # Order-related views
    path('order/', views.order_summary, name='order_summary'),  # Order page with pseudo payment
	path('order/add-item/', views.order_add_item, name='order_add_item'),
    path('ordersuccess/', views.order_success, name='order_success'),  # Successful order page
]
