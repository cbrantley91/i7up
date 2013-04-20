import sys
import re
import nltk
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

#Grabs the raw line, includes whitespace
#Returns a list of the text broken up by newlines
def getRawSentences(text):
   sents = []
   curr_string = ''
   while text:
      curr_string += text[0]
      if text[0] == '\n':
         sents.append(curr_string)
         curr_string = ''
      text = text[1:]
   return sents

#Uses nltk to break text into sentences, removes whitespace
#Returns a list of text broken up by sentences
def breakTextIntoSentences(text):
   return [sent.strip() for sent in tokenizer.tokenize(text,      \
         realign_boundaries = True)]

#Goes through the list and tries to find the braces in each sentence
#Returns a list of the braces and another list with braces stripped off
def readSentences(strList):
   strLine = ''
   newLine = ''
   gList = []
   aList = []

   for str in strList:
      strLine = str
      #if strLine.find('\"') >= 0 and strLine.rfind('\"') >= 0 and \
      #   strLine.startswith('Understand') < 0:
      #   strLine = strLine[:strLine.find('\"')-1] +               \
      #             strLine[strLine.rfind('\"')+1:]
      #   if strLine.startswith('\"'):
      #      strLine = ''
      #if strLine.find('[') >= 0 and strLine.find(']') >= 0:
      #   strLine = strLine[:strLine.find('[')-1] + strLine[strLine.find(']')+1:]
      #   if strLine.startswith('['):
      #      strLine = ''
      #if strLine.find('(') >= 0 and strLine.find(')') >= 0:
      #   strLine = strLine[:strLine.find('(')-1] + strLine[strLine.find(')')+1:]
      #   if strLine.startswith('('):
      #      strLine = ''
      #if strLine.find('{') >= 0 and strLine.find('}') >= 0:
         #if strLine.find('|') >= 0 and strLine.find(':') >= 0:
      if 'left' in strLine and '{' in strLine and '}' in strLine:
         print 'left FOUND : ', strLine

      if '{' in strLine and '}' in strLine:
         newLine = strLine[strLine.find("{"):strLine.find("}")+1]
         aList.append(newLine)
         gList.append(newLine.strip('{}'))
   return aList, gList

#Takes in a list raw sentences and a list of the braces found in the text
#Returns a string of the entire text with braces replaced with first word
def formatFile(braceList, rSent):
   str = ''

   for rsent in rSent:
      str += rsent
   for bsent in braceList:
      str = str.replace(bsent, findFirstWord(bsent.strip('{}')).strip())

   return str

#Grabs the first word to be used to replace the braces in text
#Returns a string of the first word
def findFirstWord(aStr):
   fWord = ' '
   words = aStr.split()

   for word in words:
      if word == ':':
         break
      else:
         fWord += word + ' '

   return fWord

#Parses the sentences to find the part of speech with synonyms
#Returns a list of understand statements
def parseSentence(str):
   wList = []
   genList = []
   words = str.split()
   aStr = ''
   bStr = ''
   i = 0

   #Cycle through each word in the sentence
   for word in words:
      if word == ':':
         bStr = aStr
         i = 0
         continue
      elif word == '|':
         wList.append(aStr)
         i = 0
         continue
      else:
         if i == 0:
            aStr = word
         else:
            aStr += ' ' + word
         i += 1
   wList.append(aStr)

   for word in wList:
      genList.append('Understand "' + word + '" as ' + bStr + '.')

   return genList
