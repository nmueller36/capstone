from django.conf.urls import url

from . import views

app_name = 'workstudy'

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^login/$', views.login_page, name="login"),
	url(r'^logout/$', views.user_logout, name="logout"),
	url(r'^process-login/$', views.process_login, name="process_login"),
	url(r'^application/$', views.application, name="application"),
	url(r'^application/completed/$', views.application_completed, name="application-completed"),
	url(r'^add_site_info/$', views.site_information, name="add_site_info"),
	url(r'^student_applications/$', views.search, name="search"),
	url(r'^student_placements/$', views.student_placement_search, name="student_placement_search"),
	url(r'^site_info/$', views.site_info_search, name="site_info_search"),
	url(r'^placement/$', views.placement, name="placement"),
	url(r'^add_site_info/completed/$', views.new_site_completed, name="new_site"),
	url(r'^user/info/$', views.display_student, name="display_student"),
	url(r'^site/info/$', views.display_site, name="display_site"),
	#url(r'^user/info/edit/$', views.edit_student, name="edit_student"),
	url(r'^edit_student/$', views.edit_student, name="edit_student"),
	url(r'^edit_completed/$', views.edit_complete, name="edit_completed")

]
