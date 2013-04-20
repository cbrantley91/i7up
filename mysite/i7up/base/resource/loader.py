import i7up.base.annotator.a_parser as ap

message="Loading sentence formats"

def getFormats(fmtFile):
    text = fmtFile.read().split('----------------------------------------\n')
    return (ap.parseAllIntoFormatList(ap.breakTextIntoSentences(text[0])),    \
            ap.parseAllIntoFormatList(ap.breakTextIntoSentences(text[1])))
    #return ap.parseAllIntoFormatList(ap.breakTextIntoSentences(fmtFile.read()))
