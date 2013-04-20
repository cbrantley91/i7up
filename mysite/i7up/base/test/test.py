import annotator.a_parser as ap

fsent = 'This <n> is a <i> and a <i>'
frmt = ap.parseIntoFormat(fsent)
text = 'This sentence is a thing and a place'
sents = ap.getTaggedSentences(text)

print ap.checkMatchFormat(frmt, sents[0])
