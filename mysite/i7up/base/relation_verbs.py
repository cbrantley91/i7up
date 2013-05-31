import en
import nltk.data

def main(rawText):
   output = []
   modifiedStr = ''
   tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
   sentences = tokenizer.tokenize(rawText.strip())

   for sentence in sentences:
      if sentence.find('The verb to') == 0:
         words = sentence.split(' ')
         if words[3] == 'be':
            continue
         else:
            if sentence.find('(') != -1 & sentence.find(')') != -1:
               modifiedStr = sentence.replace(sentence[sentence.find('(') \
                             :sentence.find(')')+1], configureVerb(words[3]))
            else:
               words.insert(4, configureVerb(words[3]))
               modifiedStr = ' '.join(words)
            output.append(('to ' + words[3], configureVerb(words[3]), sentence,
                           modifiedStr))
   return output

def configureVerb (verb):
   conjugatedVerbList = []
   str = ''
   infinitive = ''
   conjugation = ''

   try:
      conjugatedVerbList.append('he ' + en.verb.present(verb, person=3))
      conjugatedVerbList.append('they ' + en.verb.present(verb, person='*'))
      conjugatedVerbList.append('he ' + en.verb.past(verb))
      conjugatedVerbList.append('it is ' + en.verb.past_participle(verb))
      conjugatedVerbList.append('he is ' + en.verb.present_participle(verb))
      conjugation = ', '.join(conjugatedVerbList)
      str = '(' + conjugation + ')'
   except:
      conjugatedVerbList = []
      pass
   
   return str

def configureNoun(tuple):
  pluralNounList = []
  noun = en.noun.singular(tuple[0])

  if(noun != tuple[0]):
     for word in tuple[1]:
        pluralNounList.append(en.noun.plural(word))

  return pluralNounList
