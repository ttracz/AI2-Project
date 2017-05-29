from django.conf.urls import include, url
from django.contrib import admin
from django.template import RequestContext
from django.contrib import admin
from myapp import views as v

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', v.index),
    url(r'^wykres_predykcji', 'myapp.plots.prediction'),
    url(r'^wykres_danych', 'myapp.plots.showplot'),
]
