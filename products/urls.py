from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    # int is used so that add string is not interpretted as product id
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
]
