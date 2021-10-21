from django.urls import path
from logistic import views as stock_view
app_name = 'logistic'
urlpatterns = [
    path('get_monthly_active/', stock_view.get_monthly_active, name = "get_monthly_active"),
    path('get_advance_declined/', stock_view.get_advance_declined, name = "get_advance_declined"),
    path('get_top_gainer/', stock_view.get_top_gainer, name = "get_top_gainer"),
    path('get_top_loosers/', stock_view.get_top_loosers, name = "get_top_loosers"),
    path('get_history_data/', stock_view.get_history_data, name = "get_history_data"),
    path('get_realtime_data/', stock_view.get_realtime_data, name = "get_realtime_data"),
]