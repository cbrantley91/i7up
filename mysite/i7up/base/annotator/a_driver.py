import sys
import a_parser
import a_evaluator

# Main below
print 'Input file: ', str(sys.argv[1])
print 'Output file: ', str(sys.argv[2])
ifile = open(sys.argv[1], 'r')
ofile = open(sys.argv[2], 'w')

while True:
    str = parser.readParsableSentence(ifile)

    if not str:
        break

    upair = parser.testUnderstandFormat(str)

    if upair:
        print evaluator.evalPhrase(upair[0]).lemma_names

    # print '+++++++++++++++++++++++++++++++++++++'

ifile.close()
ofile.close()
