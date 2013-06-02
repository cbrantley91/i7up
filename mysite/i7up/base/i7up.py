#!/usr/bin/python
import annotator.loader as rldr
import annotator.a_parser as ap
import annotator.a_evaluator as ae
import sys
import nltk
import generator.driver as gd
#import argparse
import optparse

print rldr.message

def stripDets(t_list):
    for index in range(len(t_list)):
#        print 'POS : ', t_list[index][1]
        if t_list[index][1] != 'DET':
#            print 'RECEIVED : ', t_list
#            print 'RETURNING : ', t_list[index:]
            return t_list[index:]
    return []

def generate(rawText, fileFlag=2):
   return gd.main(rawText, fileFlag)

def objgen(intext):
    r_sents = ap.getRawSentences(intext)
    t_sents = ap.getTaggedSentences(r_sents)
    assert len(r_sents) == len(t_sents)
    rt_pairs = zip(r_sents, t_sents)

    r_sents = []
    out_list = []
    used_words = []
    objStr = ''
    objlist = []

    for pair in rt_pairs:
        r_sent = pair[0]
        t_sent = pair[1]
        blacklisted = False

        for fmt in bfmts:
            if ap.checkMatchFormat(fmt, t_sent):
                blacklisted = True
                break

        if not blacklisted:
            for fmt in wfmts:
                res = ap.checkMatchFormat(fmt, t_sent)
                if res:
                #cut off things until a valid phrase is found
                    evPhrase = ([], res[0], [])
                    evalRes = ae.evalFirstSyn([word[0] for word in evPhrase[1]])
                    evalObj = ae.evalObject([word[0] for word in evPhrase[1]])
                    while not evalRes and evPhrase[1] and not evalObj:
                        stripped = ap.stripTagset(evPhrase[1])
                        evPhrase = (evPhrase[0] + stripped[0], stripped[1],
                                    stripped[2] + evPhrase[2])
#                        evalRes = ae.evalFirstSyn([word[0] for word in evPhrase[1]])
                        evalObj = ae.evalObject([word[0] for word in evPhrase[1]])
                        #objStr += ' '.join([wt_pair[0] for wt_pair in evPhrase[1]]) + '\n'
                        #objStr += str(evalObj).strip('[]')
                        #objStr = objStr.replace(', ', '\n')
                        #objStr += '\n\n'
                        #temp : to deal with proper noun issues
                        if 'NNP' in [word[1] for word in evPhrase[1]]:
                            break
#                        s_list = evalRes

#                        w_orig = ' '.join([wt_pair[0] for wt_pair in evPhrase[1]])

                        currw = '_'.join([wt_pair[0] for wt_pair in evPhrase[1]])

                        #TODO REIMPLEMENT CHECK TO MAKE SURE NOT A DUPLICATE (cbrantle)
#                        if currw in s_list:
#                            s_list.remove(currw)

                        if currw in used_words:
                            break

                        if not evalObj:
                            break

                        used_words.append(currw)

                        if evalObj:
                            objlist.append(currw)

                        repl_sent = ''
                        repl_sent += '<button type=\'button\' id="' + currw +   \
                                     '" class="btn btn-info" onclick=' +        \
                                     '"javascript:expColl(\'' + currw +         \
                                     '_wrapper\')">' + currw.replace('_', ' ') + '</button>'
                        repl_sent += '<div id=' + currw + '_wrapper style=' +   \
                                     '"overflow:hidden;display:none"><br /><pre>'
                        curr_lemma_list = []
                        for syn in evalObj:
                            syn_text = '<p><b>' + syn.definition + '</b><br />'
                            curr_syn_tot = 0
                            for lemma in syn.lemma_names:
                                if lemma not in curr_lemma_list and lemma != currw:
                                    syn_text += '<input type="checkbox" name="' + \
                                                 'syn|' + currw +'" value="' + lemma +    \
                                                 '"> ' + lemma.replace('_', ' ') \
                                                 + '</input><br />'
                                    curr_lemma_list += lemma
                                    curr_syn_tot += 1

                            syn_text += '</p>'

                            if curr_syn_tot == 0:
                                continue

                            repl_sent += syn_text

                                #repl_sent += '<input type="radio" name="' + currw + '" value="' + str(syn) + '"> ' + ' | '.join(syn.lemma_names) + '<br>'
#                        repl_sent = '{ ' + ' '.join([wt_pair[0] for wt_pair in evPhrase[1]]) + \
#                            ' : ' + ' | '.join(s_list) + ' }'
#                        repl_sent = '{{ ' + ' '.join([wt_pair[0] for wt_pair in evPhrase[1]]) + ' }}'
#                        repl_sent = repl_sent.replace('_', ' ')
                        repl_sent += '</pre></div>'
                        #repl_sent += '<a href="javascript:expColl(\'' + currw + '_wrapper\',\'none\')">Hide</a>'
                        #repl_sent += '<a href="javascript:expColl(\'' + currw + '_wrapper\',\'block\')">Expand</a>'

                        if not curr_lemma_list:
                            break

                        if currw == 'type':
                            break

                        r_sent = r_sent.replace(' '.join([word[0] for word in  \
                         evPhrase[1]]), repl_sent)

                        break

        out_list.append(r_sent)

    s = ''
    for string in out_list:
        s += string
    return (s, objlist)

def get_opts(intext):
    r_sents = ap.getRawSentences(intext)
    t_sents = ap.getTaggedSentences(r_sents)
    assert len(r_sents) == len(t_sents)
    rt_pairs = zip(r_sents, t_sents)

    r_sents = []
    out_list = []
    used_words = []
    objStr = ''
    objlist = []

    for pair in rt_pairs:
        r_sent = pair[0]
        t_sent = pair[1]
        blacklisted = False

        for fmt in bfmts:
            if ap.checkMatchFormat(fmt, t_sent):
                blacklisted = True
                break

        if not blacklisted:
            for fmt in wfmts:
                res = ap.checkMatchFormat(fmt, t_sent)
                if res:
                #cut off things until a valid phrase is found
                    evPhrase = ([], res[0], [])
                    evalRes = ae.evalFirstSyn([word[0] for word in evPhrase[1]])
                    evalObj = ae.evalObject([word[0] for word in evPhrase[1]])
                    while not evalRes and evPhrase[1] and not evalObj:
                        stripped = ap.stripTagset(evPhrase[1])
                        evPhrase = (evPhrase[0] + stripped[0], stripped[1],     \
                                    stripped[2] + evPhrase[2])
                        evalRes = ae.evalFirstSyn([word[0] for word in          \
                                                   evPhrase[1]])
                        evalObj = ae.evalObject([word[0] for word in            \
                                                 evPhrase[1]])

                        if evalRes and evalObj:
                            objlist.append((' '.join([wt_pair[0] for wt_pair in \
                                                      evPhrase[1]]), evalObj))

                        if 'NNP' in [word[1] for word in evPhrase[1]]:
                            break
                        s_list = evalRes

                        w_orig = ' '.join([wt_pair[0] for wt_pair in            \
                                           evPhrase[1]])
                        if s_list and w_orig in s_list:
                            s_list.remove(w_orig)

                        if not s_list:
                            break

                        if w_orig in used_words:
                            break

                        used_words.append(w_orig)

                        repl_sent = '{ ' + ' '.join([wt_pair[0] for wt_pair in  \
                            evPhrase[1]]) + ' : ' + ' | '.join(s_list) + ' }'

                        repl_sent = repl_sent.replace('_', ' ')

                        #temp : to deal with font settings being evaluated
                        if 'type' in repl_sent:
                            break

                        r_sent = r_sent.replace(' '.join([word[0] for word in  \
                         evPhrase[1]]), repl_sent)

                        break

#       out_list.append(r_sent)

    s = ''
    for string in out_list:
        s += string
    return objlist

if __name__ != '__main__':
    fmtFile = './i7up/base/resource/sFormats.in'
else:
    fmtFile = './resource/sFormats.in'

    usage = 'i7up.py [options] INPUT'
    parser = optparse.OptionParser(usage=usage)

#    parser.add_option('-i', '--input', action='store', type='string', dest='i', help='specify input file')
    parser.add_option('-o', '--output', action='store', type='string', dest='o', default='gen.out', help='specify output file')
    parser.add_option('-a', '--action', action='store', type='string', dest='a', default='full', help='specify action (full, annotate, generate)')
    parser.add_option('-f', '--formats', action='store', type='string', dest='sf', default='./resource/sFormats.in', help='specify format file')

    (options, args) = parser.parse_args()

ffile = open(fmtFile, 'r')

# Get formats
fmts = rldr.getFormats(ffile)

    #TODO, change so it returns both
bfmts = fmts[0]
wfmts = fmts[1]
ffile.close()

if __name__ == '__main__':
#    if not options.i:
#       print usage
#       quit()
    if not args:
       print 'missing file operand'
       print "try `i7up.py -h' for more information"
       quit()

    if options.a == 'full' or options.a == 'annotate':
        annotate(args[0], options.o, options.sf)
#        annotate(arg[0])

    if options.a == 'full':
        generate(options.o, options.o)

    if options.a == 'generate':
        generate(args[0], options.o)

    if options.a == 'objgen':
        ifile = open(args[0], 'r')
        ofile = open(options.o, 'w')

        ofile.write('<!DOCTYPE html><head></head><body><pre>' + objgen(ifile.read())[0] + '</pre></body>')
        ifile.close()
        ofile.close()

