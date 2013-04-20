#!/usr/bin/python
import resource.loader as rldr
import annotator.a_parser as ap
import annotator.a_evaluator as ae
import sys
import nltk
import generator.driver as gd
#import argparse
import optparse

print rldr.message

fmtFile = './i7up/base/resource/sFormats.in'
ffile = open(fmtFile, 'r')

# Get formats
fmts = rldr.getFormats(ffile)

    #TODO, change so it returns both
bfmts = fmts[0]
wfmts = fmts[1]
ffile.close()

def stripDets(t_list):
    for index in range(len(t_list)):
#        print 'POS : ', t_list[index][1]
        if t_list[index][1] != 'DET':
#            print 'RECEIVED : ', t_list
#            print 'RETURNING : ', t_list[index:]
            return t_list[index:]
    return []

def generate(infile, outfile, fileFlag=2):
   gd.main(infile, outfile, fileFlag)

def annotate(intext):
    # Get raw and tagged sentences

    r_sents = ap.getRawSentences(intext)
    t_sents = ap.getTaggedSentences(r_sents)
    assert len(r_sents) == len(t_sents)
    rt_pairs = zip(r_sents, t_sents)

#    for pair in rt_pairs:
#        print pair

    r_sents = []
    # Get items
    #items = ap.findItemsFromFormats(fmts, t_sents)

#    print '------------'
#    print 'Found Items:'
#    print '------------'

    out_list = []
    used_words = []

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
#                    evalRes = ae.evalPhrase([word[0] for word in evPhrase[1]])

                    while not evalRes and evPhrase[1]:
                        stripped = ap.stripTagset(evPhrase[1])
                        evPhrase = (evPhrase[0] + stripped[0], stripped[1],
                                    stripped[2] + evPhrase[2])
                        evalRes = ae.evalFirstSyn([word[0] for word in evPhrase[1]])
#                    while not evalRes and evPhrase[1]:
#                       stripped = ap.stripTagset(evPhrase[1])
#                        evPhrase = (evPhrase[0] + stripped[0], stripped[1],                \
#                                    stripped[2] + evPhrase[2])
#                        evalRes = ae.evalPhrase([word[0] for word in evPhrase[1]])

                    if evalRes:
                        #temp : to deal with proper noun issues
                        if 'NNP' in [word[1] for word in evPhrase[1]]:
                            break
                        s_list = evalRes
#                    if evalRes:
#                        s_list = []
#                        for posType in evalRes:
#                            for dictDef in posType:
#                                for word in dictDef:
#                                    if word not in s_list:
#                                        s_list.append(word)

                        w_orig = ' '.join([wt_pair[0] for wt_pair in evPhrase[1]])
                        if w_orig in s_list:
                            s_list.remove(w_orig)

                        if not s_list:
                            break

                        if w_orig in used_words:
                            break

                        used_words.append(w_orig)

                        repl_sent = '{ ' + ' '.join([wt_pair[0] for wt_pair in evPhrase[1]]) + \
                            ' : ' + ' | '.join(s_list) + ' }'

                        repl_sent = repl_sent.replace('_', ' ')

                        #temp : to deal with font settings being evaluated
                        if 'type' in repl_sent:
                            break

                        r_sent = r_sent.replace(' '.join([word[0] for word in  \
                         evPhrase[1]]), repl_sent)

                        break

        out_list.append(r_sent)
        #print 'Raw Sentence : ', r_sent

    #print '--------------------\nFound Items\n------------------'

    #for item in items:
    #    print item

    #ofile = open(outfile, 'w')
    #for string in out_list:
    #    ofile.write(string)
    #ofile.write('\n')

    # Write copy to file
    #ofile.close()
    s = ''
    for string in out_list:
        s += string
    return s

#parser = argparse.ArgumentParser(description='Inform 7 Usability Precompiler')
#parser.add_argument('-a', default='full', help='Whether or not you want to just annotate, generate, or do both.  Input "annotate", "generate", or "full". Defaults to full.')
#parser.add_argument('-i', required=True, help='The path to the input file')
#parser.add_argument('-o', default='gen.out', help='The path and filename of the output file')
#parser.add_argument('-sf', default='./resource/sFormats.in', help='Format file for the sentences. Defaults to Inform 7.')

#usage = 'i7up.py [options] INPUT'
#parser = optparse.OptionParser(usage=usage)

#parser.add_option('-i', '--input', action='store', type='string', dest='i', help='specify input file')
#parser.add_option('-o', '--output', action='store', type='string', dest='o', default='gen.out', help='specify output file')
#parser.add_option('-a', '--action', action='store', type='string', dest='a', default='full', help='specify action (full, annotate, generate)')
#parser.add_option('-f', '--formats', action='store', type='string', dest='sf', default='./resource/sFormats.in', help='specify format file')

#(options, args) = parser.parse_args()

#if not options.i:
#    print usage
#    quit()
#if not args:
#    print 'missing file operand'
#    print "try `i7up.py -h' for more information"
#    quit()

#if options.a == 'full' or options.a == 'annotate':
#    annotate(args[0], options.o, options.sf)

#if options.a == 'full':
#    generate(options.o, options.o)

#if options.a == 'generate':
#    generate(args[0], options.o)
