import nltk
from nltk.tag.simplify import simplify_wsj_tag

#Sentence has:
# raw_sent - the raw string of the sentence
# quoted - whether or not it is a quoted sentence or not
# sub_sents - list of sentences inside this one (all should be quoted)
class Sentence:
    def __init__(self, raw, quotation = false):
        self.raw_sent = raw
        self.sub_sents = []
        self.quoted = quotation
        if '"' in raw_sent:
            raw_sent.find('"')

    def __repr__(self):
        if self.isQuoted:
            #quoted string
            r_str = '< QS : '
            for sent in sub_sents:
                r_str +=
        else:
            #source string
            r_str = '< SS : '

        r_str += '\n  Text: "' + raw_sent + '"\n'
        index = 0
        for sent in sub_sents:
            r_str += '   SubSentence ' + index + ' : "' + sent + '"\n'
        r_str += '\n'
        return r_str

def findAll(r_str, c):
    indices = []
    while r_str:
        #if index is beyond the range of the string, break
        #if index is in the string, append to indices

    #return indices

def parseSentences(text):
    r_sents = []
    0_sents = []
    curr_str = ''
    inQuote = false
    while text:
        curr_str += text[0]
        if text[0] == '"':
            text = text[1:]
            while text[0] != '"':
                curr_str += text[0]
                text = text[1:]
            curr_str += '"'
            if curr_str[-2] == '.' and text[0] == ' ':
                r_sents.append(curr_str)
                curr_str = ''
        if text[0] == '.':
            r_sents.append(curr_str)
            curr_str = ''
        text = text[1:]

    for sent in r_sents:
        print "'", sent, "'"

    for sent in sents:
        o_sents.append(Sentence(r_sent))
        print o_sents[-1]

