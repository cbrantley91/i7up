import sys
import re
import nltk
from nltk.tag.simplify import simplify_wsj_tag

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

class Placeholder:
    def __init__(self, typestr):
        self.tstr = re.sub('[<>]', '', typestr).lower();
    def __repr__(self):
        return "<PH : '" + self.tstr + "'>"
    def isPrimary(self):
        return 'n' in self.tstr or 'v' in self.tstr
    def isIdentifier(self):
        return 'i' in self.tstr

def readParsableSentence(rfile):
    while True:
        c = rfile.read(1)

        if c == '[':
            while c and c != ']':
                c = rfile.read(1)
        elif c == '"':
            str += c + readUntilEndQuote(rfile)
        elif c == '.':
            str += c
            break
        elif c:
            str += c
        else:
            break

    return str.strip()

def readUntilEndQuote(rfile):
    str = ''
    while True:
        c = rfile.read(1)

        if not c:
            break
        if c == '"':
            str += c
            break

        if c == '\\':
            str += c
            c = rfile.read(1)

        str += c

    return str

def findIndicesOfPlaceholder(wordList):
    return [i for i, x in enumerate(wordList) if isPlaceholder(x)]

def isPlaceholder(word):
    if '<' in word and '>' in word:
        return True
    return False

def parseIntoFormat(sentence):
    prevIndex = 0
    sList = []
    wordList = sentence.strip().split()

    for index in findIndicesOfPlaceholder(wordList):
        sList.append(wordList[prevIndex:index])
        sList.append(Placeholder(wordList[index]))
        prevIndex = index + 1

    sList.append(wordList[prevIndex:])
    return [x for x in sList if x != []]

def parseAllIntoFormatList(sentences):
    return [parseIntoFormat(s) for s in sentences]

#returns a list of formats to be parsed
def retrieveFormatsFromFile(iFileName):
    fmtList = []

    with open(iFileName) as iFile:
        line = iFile.readline()
        while line:
            fmtList.append(parseIntoFormat(line))
            line = iFile.readline()

    return fmtList

def checkMatchFormat(frmt, sentence):
    primary = []
    idents = []

    while frmt:
        if isinstance (frmt[0], Placeholder):
            if len(frmt) > 1:
                found = False
                #more afterwards
                for index in [i for i, x in enumerate(sentence) if x[0] ==     \
                 frmt[1][0]]:
                    if [word[0] for word in sentence[index:index +             \
                     len(frmt[1])]] == frmt[1]:
                        if frmt[0].isPrimary():
                            typestr = frmt[0].tstr
                            primary = sentence[:index]
                        elif frmt[0].isIdentifier():
                            idents.append(sentence[:index])

                        sentence = sentence[index + len(frmt[1]):]
                        found = True
                        break
                if not found:
                    return None
                frmt = frmt[2:]

            else:
                #end of format - rest is for identifier
                if frmt[0].isPrimary():
                    typestr = frmt[0].tstr
                    primary = sentence
                elif frmt[0].isIdentifier():
                    idents.append(sentence[:index])

                frmt = frmt[1:]
        else:
            #some basic text to match at start
            if frmt[0] != [word[0] for word in sentence[:len(frmt[0])]]:
                return None
            sentence = sentence[len(frmt[0]):]
            frmt = frmt[1:]

    return primary, idents

#def breakTextIntoSentences(text):
#    return [nltk.word_tokenize(sent.strip().strip('.')) for sent in         \
#     tokenizer.tokenize(text)]

def breakTextIntoSentences(text):
    return [sent.strip().strip('.') for sent in tokenizer.tokenize(text)]

def getRawSentences(text):
    sents = []
    curr_string = ''
    while text:
        curr_string += text[0]
        if text[0] == '"':
            text = text[1:]
            while text[0] != '"':
                curr_string += text[0]
                text = text[1:]
            curr_string += '"'
        if text[0] == '.':
            sents.append(curr_string)
            curr_string = ''
        text = text[1:]

    sents.append(curr_string);

    return sents

def findItemsFromFormats(frmts, sents):
    foundItems = []

    for sent in sents:
        for frmt in frmts:
            res = checkMatchFormat(frmt, sent)

            if res:
                foundItems.append(res)
                break

    return foundItems

def getTaggedSentences(sentences):
#   simpList = []
#   sentences = [nltk.pos_tag(nltk.word_tokenize(sent)) for sent in sentences]
#   for tagsent in sentences:
#      simpList.append([(word, simplify_wsj_tag(tag)) for word, tag in tagsent])
#return sentences
#   return simpList
   return [nltk.pos_tag(nltk.word_tokenize(sent)) for sent in sentences]

def removeTag (tupList):
   return [tup for tup in tupList if tupSig(tup)]

#Add what you want to remove here
def tupSig (tup):
   if tup[1] == 'DT' or tup[1] == '\'\'' or tup[1] == 'IN' or                   \
    tup[1] == '``' or tup[1] == 'WDT':
      return False
   else:
      return True

def stripTag (tupList):
   tagHierarchy = {':' : 1, '``' : 2, '\'\'' : 3, '\"\"' : 4, '.' : 5, 'DT' : 6,      \
      'WDT' : 7, 'TO' : 7, 'VBZ': 7, 'JJ': 8, 'CD' : 8, 'IN' : 9, 'NN' : 9,    \
      'VB' : 9, 'NNP' : 9, 'VBG' : 9, 'NNS' : 9}
#   tagHierarchy = {'``': 1, 'ADJ' : 8, 'ADV' : 8, 'CNJ' : 4, 'DET': 3,       \
#      'EX' : 4, 'FW' : 8, 'MOD' : 7, 'N' : 10, 'NP' : 9, 'NUM' : 3,          \
#      'PRO' : 9, 'P' : 7, 'TO' : 2, 'UH' : 8, 'V' : 10, 'VD' : 10,           \
#      'VG' : 9, 'VN' : 9, 'WH' : 7, '\'\'' : 1, ':' : 1, '.' : 1}

   frontList = []
   midList = []
   endList = []
   tup = tupList[0]
   tupEnd = tupList[len(tupList)-1]

   if tagHierarchy[tup[1]] == tagHierarchy[tupEnd[1]]:
      endList.append(tupEnd)
      del tupList[len(tupList)-1]
   elif tagHierarchy[tup[1]] > tagHierarchy[tupEnd[1]]:
      endList.append(tupEnd)
      del tupList[len(tupList)-1]
   else:
      frontList.append(tup)
      del tupList[0]

   for count in tupList:
      midList.append(count)
   return frontList, midList, endList

def stripTagset (tupList):
   tagHierarchy = [('$', 1), ('\'\'', 1), ('(', 1), (')', 1), (',', '1'),      \
      ('--', 1), ('.', 1), (':', 1), ('``', 1), ('CC', 2), ('CD', 3),          \
      ('CC', 2), ('CD', 2), ('DT', 3), ('EX', 2), ('FW', 4), ('IN', 3),        \
      ('JJ', 7), ('LS', 2), ('MD', 3), ('NN', 8), ('POS', 2), ('PRP', 3),      \
      ('RB', 7), ('RP', 5), ('SYM', 1), ('TO', 2), ('UH', 3), ('VB', 8),       \
      ('WP', 3)]
   frontList = []
   midList = []
   endList = []
   tupFront = tupList[0]
   tupEnd = tupList[len(tupList)-1]
   tupFrontNdx = 0
   tupEndNdx = 0

   for tupl in tagHierarchy:
      if tupl[0] in tupFront[1]:
         tupFrontNdx = tupl[1]
      if tupl[0] in tupEnd[1]:
         tupEndNdx = tupl[1]

   if tupFrontNdx == tupEndNdx:
      endList.append(tupEnd)
      del tupList[len(tupList)-1]
   elif tupFrontNdx > tupEndNdx:
      endList.append(tupEnd)
      del tupList[len(tupList)-1]
   else:
      frontList.append(tupFront)
      del tupList[0]

   for count in tupList:
      midList.append(count)

   return frontList, midList, endList
