from django.urls import path
from django.conf.urls import url
from logistic import views as stock_view
app_name = 'logistic'
urlpatterns = [
    url(r'^$',stock_view.home, name="home"),
    url(r'^logistic/get_monthly_active/$', stock_view.get_monthly_active, name = "get_monthly_active"),
    url(r'^logistic/get_advance_declined/$', stock_view.get_advance_declined, name = "get_advance_declined"),
    url(r'^logistic/get_top_gainer/$', stock_view.get_top_gainer, name = "get_top_gainer"),
    url(r'^logistic/get_top_loosers/$', stock_view.get_top_loosers, name = "get_top_loosers"),
    url(r'^logistic/get_history_data/$', stock_view.get_history_data, name = "get_history_data"),
    url(r'^logistic/get_realtime_data/$', stock_view.get_realtime_data, name = "get_realtime_data"),
]