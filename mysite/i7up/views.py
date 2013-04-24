from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from i7up.models import MyChoice, MyPoll
import base.i7up as i7

def results(request):
    #p = get_object_or_404(MyPoll, pk=poll_id)
    i7code = request.POST['i7code']
    if i7code == 'Input your I7 Source here...':
        return render(request, 'i7up/detail.html', {
                'error_message' : "You didn't input your code!"
                })
    else:
        return render(request, 'i7up/detail.html', {
                'opts' : i7.annotate(i7code.encode("utf8","ignore"))
                })
#        return HttpResponseRedirect(reverse('i7up:result', args=(i7code,)))
