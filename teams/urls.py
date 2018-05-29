from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'teams'
urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('activate/<uid>/<token>', views.activate, name='activate'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('user/<int:pk>', views.profile_detail_with_pk, name='profile_pk'),
    path('user/profile', views.profile_detail, name='profile'),
    path('user/profile/edit', views.profile_edit, name='profile_edit'),
    path('user/applications', views.application_list, name='applications'),
    path('user/applications/<int:pk>/accept',
         views.accept_application,
         name='accept_application'),
    path('user/applications/<int:pk>/reject',
         views.reject_application,
         name='reject_application'),
    path('user/notifications', views.notifications, name='notifications'),
    path('user/notifications/mark_as_read',
         views.mark_as_read,
         name='mark_as_read'),
    path('project/new', views.project_edit, name='project_new'),
    path('project/<int:pk>', views.project_detail, name='project'),
    path('project/<int:pk>/edit', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete',
         views.project_delete,
         name='project_delete'),
    path('project/<int:pk>/apply/<int:project_position_pk>',
         views.apply,
         name='apply'),
    path('positions/<int:position_pk>', views.home, name='position_filter'),
    path('positions/<fillable>', views.home, name='fillable'),
    path('search', views.search, name='search'),
    path('', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
