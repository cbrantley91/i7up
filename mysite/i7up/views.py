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
        htmlgentext, l_opts = i7.objgen(i7code)
        v_opts = []

        # TODO FIX!!!
        r_verbs = rv.main(i7code)
        for v_phrase, conj_phrase, pre_repl, post_repl in r_verbs:
#            htmlgentext = htmlgentext.replace(pre_repl, '<button type=\'button\' class="btn btn-success" id="' + v_phrase.replace(" ", "_") + '">' + post_repl + '</button>')
            htmlgentext = htmlgentext.replace(pre_repl, pre_repl.replace(v_phrase, '<button type=\'button\' class="btn btn-success" id="' + v_phrase.replace(" ", "_") + '" onclick="javascript:toggleConj(\'' + v_phrase.replace(" ", "_") + '\')" repltext="' + v_phrase + ' ' + conj_phrase + '">' + v_phrase + '</button>') + '<script> $(\'#' + v_phrase.replace(' ', '_') + '\').click(function() {var temp = $(this).text(); $(this).text($(this).attr(\'repltext\')); $(this).attr(\'repltext\', temp);});</script>')
            v_opts.append(v_phrase.replace(" ", "_"))

        endtempstr = str(r_verbs)
        htmlgentext = '<pre class="prew">' + htmlgentext + '</pre>'

        return render(request, 'i7up/html-genned.html', {
            'is_opts' : l_opts or v_opts,
            'l_opts' : l_opts,
            'v_opts' : v_opts,
            'htmlgentext' : htmlgentext
        })
    else:
        e_message = ''
        if request.session:
            if request.method == 'POST' and 'rawcode' in request.session:
                e_message = request.session['rawcode']
            request.session.delete()

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


