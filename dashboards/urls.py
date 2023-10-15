from django.urls import path

from . import views

urlpatterns = [
    path("input-price-chart", views.input_price_chart, name="input-price-chart"),
]
