import sys
import parser
import random

def main(infile, outfile, fileFlag):
   ifile = open(infile, 'r')
   text = ifile.read()
   ifile.close()
   ofile = open(outfile, 'w')

   rSent = parser.getRawSentences(text)
   sentences = parser.breakTextIntoSentences(text)
   braceList, gList = parser.readSentences(sentences)
   ofile.write(parser.formatFile(braceList, rSent))
   if fileFlag == 1 or fileFlag == 2:
      ofile.write('\n[Generated Statements Below]\n')
      for line in gList:
         uSent = parser.parseSentence(line)
         if fileFlag == 1:
            uSent = [uSent[random.randint(0, len(uSent)-1)]]
         for uline in uSent:
            ofile.write(uline + '\n')
   ofile.close()

