from django.conf.urls import url
from . import views

# Must include links to the
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^success', views.success),
    url(r'^process_quote', views.process_quote),
    url(r'^delete_quote', views.delete_quote),
    url(r'^user/(?P<id>\d+)', views.user_info),
    url(r'^myaccount/(?P<id>\d+)', views.update_info, name="edit_user"),
    url(r'^update', views.process_update),
    url(r'^like_quote', views.like_quote),

]