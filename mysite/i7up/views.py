from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from i7up.models import MyChoice, MyPoll
import base.i7up as i7

#def index(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
#    context = {'latest_poll_list': latest_poll_list}
#    return render(request, 'polls/index.html', context)

#def detail(request, poll_id):
#    poll = get_object_or_404(Poll, pk=poll_id)
#    return render(request, 'polls/detail.html', {'poll': poll})

#def results(request, poll_id):
#    poll = get_object_or_404(Poll, pk=poll_id)
#    return render(request, 'polls/results.html', {'poll': poll})

def results(request):
    #p = get_object_or_404(MyPoll, pk=poll_id)
    i7code = request.POST['i7code']
    if i7code == 'Input your I7 Source here...':
        return render(request, 'i7up/detail.html', {
                'error_message' : "You didn't input your code!"
                })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request, 'i7up/detail.html', {
                'result_message' : i7.annotate(i7code.encode("utf8","ignore"))
                })
#        return HttpResponseRedirect(reverse('i7up:result', args=(i7code,)))
