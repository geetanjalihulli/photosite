from django.conf.urls import patterns, include, url
#from settings import MEDIA_ROOT, DEBUG, MEDIA_URL
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls))
)

urlpatterns += patterns('formapp.views',
    (r'^login/$', 'login_user', {'login_template' : 'fapp/login.html'}, 'login'),
    (r'^register/$', 'register_user', {'register_template' : 'fapp/register.html'}, 'register'),
    (r'^home/$', 'home_page', {'logged_in_template': 'fapp/logged_in.html'}, 'home'),
    (r'^logout/$', 'logout_page', {'log_out_template': 'fapp/login.html'}, 'logout'),
    (r'^upload/(?P<album_name>[a-zA-Z]*)$', 'upload_photo_page', {'upload_photo_template': 'fapp/upload_photo.html'}),
    (r'^new_album/$', 'create_album_page', {'new_album_template': 'fapp/create_album.html'}, 'new_album'),
    (r'^album/(?P<album_name>[a-zA-Z]+)$', 'display_album_page', {'display_album_template': 'fapp/display_album.html'}),
)

#import pdb;pdb.set_trace()
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^home/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
   )

#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Formapp.views.home', name='home'),
    # url(r'^Formapp/', include('Formapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
#)
