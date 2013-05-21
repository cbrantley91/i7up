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
        htmlgentext, topts = i7.objgen(i7code)
        htmlgentext = '<pre class="prew">' + htmlgentext + '</pre>'
#        htmlgentext = htmlgentext.replace('\n', '<br />')
        return render(request, 'i7up/html-genned.html', {
# TODO change opts to returned
            'opts' : i7.get_opts(i7code.encode("utf8","ignore")),
            'htmlgentext' : htmlgentext
        })
    else:
        e_message = ''
        for i, x in request.POST.iteritems():
            try:
                #for lemma in x:
                if i == 'csrfmiddlewaretoken':
                    continue
                l_list = request.POST.getlist(i.rstrip('[]'))
                for lemma in l_list:
                    e_message += 'Understand "' + lemma + '" as ' + i.rstrip('[]') + '.\n'
            except AttributeError:
                pass
            #print str(request.POST);
        return render(request, 'i7up/html-genned.html', {
            'error_message' : e_message,
            'pageurl' : request.get_full_path()
        })

def gen_page(request):
    return render(request, 'i7up/html-genned.html', {})

def about_page(request):
    return render(request, 'i7up/about.html', {})

def contact_page(request):
    return render(request, 'i7up/contact.html', {})

