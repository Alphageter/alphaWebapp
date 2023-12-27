from django.urls import path , re_path
from . import views
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView , LogoutView

urlpatterns = [
        path('login/', LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
        path('logout/', LogoutView.as_view(template_name='login.html'), name='logout'),
        path('dashboard/',views.dashboard , name='dashboard'),
        path('search_orders/', views.search_orders, name='search_orders'),
        path('order/<int:id>/', views.order_detail, name='order_detail'),
        path('dashboard/<date>/', views.dashboard_by_date, name='dashboard_by_date'),
        path('statistic/', views.get_statistic, name='get_statistic'),
        path('test/', views.chart_data_int, name='chart_data_int'),
        path('select_cahrtdates/', views.select_cahrtdates, name='select_cahrtdates'),
        path('type_chartdata/', views.type_chartdata, name='type_chartdata'),
        path('get_orders/', views.get_orders, name='get_orders'),
        

]