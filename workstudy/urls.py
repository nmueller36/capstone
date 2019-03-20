from django.conf.urls import url

from . import views

app_name = 'workstudy'

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^application/$', views.application, name="application"),
	url(r'^application/completed/$', views.application_completed, name="application-completed"),
	url(r'^add_site_info/$', views.site_information, name="add_site_info"),
	url(r'^results/$', views.search, name="search")
]
