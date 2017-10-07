"""apis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from apis.v1 import views

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
#router.register(r'irctc.new_order', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^v1.orders.create$', views.OrdersView.create), 
    url(r'^v1.orders.cancel$', views.OrdersView.cancel), 
    url(r'^v1.orders.update$', views.OrdersView.update), 
    url(r'^v1.orders.list$', views.OrdersView.list), 
    url(r'^v1.orders.set_status$', views.OrdersView.set_status), 

    url(r'^v1.restaurants.create$', views.RestaurantView.create),
    url(r'^v1.restaurants.update$', views.RestaurantView.update),
    url(r'^v1.restaurants.list$', views.RestaurantView.list),
    url(r'^v1.restaurants.delete$', views.RestaurantView.delete),

    url(r'^v1.boys.create$', views.BoysView.create),
    url(r'^v1.boys.update$', views.BoysView.update),
    url(r'^v1.boys.list$', views.BoysView.list),
    url(r'^v1.boys.delete$', views.BoysView.delete),
    url(r'^v1.boys.send_login_otp$', views.BoysView.send_login_otp),

    url(r'^v1.boys.get_launch_data$', views.BoysView.get_launch_data),
]

