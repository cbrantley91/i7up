from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from i7up.models import MyPoll
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=MyPoll.objects.order_by('-pub_date')[:5],
            context_object_name='latest_poll_list',
            template_name='i7up/temp.html'),
        name='index'),
    #url(r'^(?P<pk>\d+)/$',
    #    DetailView.as_view(
    #        model=MyPoll,
    #        template_name='i7up/detail.html'),
    #    name='detail'),
    #url(r'^(?P<pk>\d+)/results/$',
    #    DetailView.as_view(
    #        model=MyPoll,
    #        template_name='i7up/results.html'),
    #    name='results'),
    url(r'^results/$', 'i7up.views.results', name='results'),
)
urlpatterns += staticfiles_urlpatterns()

