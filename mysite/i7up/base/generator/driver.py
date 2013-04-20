import sys
import parser
import random

def main(rawText, fileFlag):
   genText = ''

   sentences = parser.breakTextIntoSentences(rawText)
   braceList, gList = parser.readSentences(sentences)
   genText = parser.formatFile(braceList, rawText);
   if fileFlag == 1 or fileFlag == 2:
      genText += '\n\n[Generated Statements Below]\n'
      for line in gList:
         uSent = parser.parseSentence(line)
         if fileFlag == 1:
            uSent = [uSent[random.randint(0, len(uSent)-1)]]
         for uline in uSent:
            genText += uline + '\n'

   return genText;
