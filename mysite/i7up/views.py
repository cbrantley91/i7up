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

    if i7code:
        request.session['rawcode'] = i7code
        return render(request, 'i7up/detail.html', {
            'opts' : i7.get_opts(i7code.encode("utf8","ignore"))
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
            'error_message' : e_message,
            'pageurl' : request.get_full_path()
        })

def gen_page(request):
    return render(request, 'i7up/detail.html', {})
