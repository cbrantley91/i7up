from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from i7up.models import MyChoice, MyPoll
import base.i7up as i7
import base.relation_verbs as rv

def results(request):
    #p = get_object_or_404(MyPoll, pk=poll_id)
    i7code = None
    if 'i7code' in request.POST:
        i7code = request.POST['i7code']

    if i7code:
        i7code = i7code.encode('ascii', 'ignore')
        request.session['rawcode'] = i7code
        htmlgentext, topts = i7.objgen(i7code)

        # TODO FIX!!!
        r_verbs = rv.main(i7code)
        for pre_repl, post_repl in r_verbs:
            htmlgentext = htmlgentext.replace(pre_repl, '<button type=\'button\' class="btn btn-success">' + post_repl + '</button>')
        endtempstr = str(r_verbs)
        htmlgentext = '<pre class="prew">' + htmlgentext + '\n-----------------------\n' + endtempstr + '</pre>'

        return render(request, 'i7up/html-genned.html', {
            'opts' : topts,
            'htmlgentext' : htmlgentext
        })
    else:
        e_message = request.session['rawcode']

        for i, x in request.POST.iteritems():
            try:
                if i == 'csrfmiddlewaretoken':
                    continue
                l_list = request.POST.getlist(i.rstrip('[]'))
                for lemma in l_list:
                    e_message += 'Understand "' + lemma + '" as ' +             \
                     i.rstrip('[]') + '.\n'
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

