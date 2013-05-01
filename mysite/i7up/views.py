from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from i7up.models import MyChoice, MyPoll
import base.i7up as i7

def results(request):
    #p = get_object_or_404(MyPoll, pk=poll_id)
    i7code = None
    if 'i7code' in request.POST:
        i7code = request.POST['i7code']
    if i7code == 'Input your I7 Source here...':
        return render(request, 'i7up/detail.html', {
                'error_message' : "You didn't input your code!"
                })
    else:
        if i7code:
            return render(request, 'i7up/detail.html', {
                'opts' : i7.annotate(i7code.encode("utf8","ignore"))
                })
        else:
            e_message = ''
            for i, x in request.POST.iteritems():
                try:
                    #for lemma in x:
                        e_message += 'Understand "' + x + '" as ' + i + '.\n'
                except AttributeError:
                    pass
            #print str(request.POST);
            return render(request, 'i7up/detail.html', {
                'error_message' : e_message
            })
#        return HttpResponseRedirect(reverse('i7up:result', args=(i7code,)))

def gen_page(request):
    for key, value in request.POST:
        return render(request, 'i7up/detail.html', {})
