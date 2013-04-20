from nltk.corpus import wordnet as wn

def evalFirstSyn(words):
   synList = []
   str = '_'.join(words)
   syn_sets = wn.synsets(str)

   if not syn_sets:
      return None
   for word in syn_sets[0].lemma_names:
      synList.append(word)

   return synList

def evalPhrase(words, pos = 'vndj'):
   str = '_'.join(words)
   vSynList = []
   nSynList = []
   adjSynList = []
   advSynList = []

   if('v' in pos):
      syn_sets = wn.synsets(str, pos = wn.VERB)
      for syn_set in syn_sets:
         vSynList.append(syn_set.lemma_names)

   if('n' in pos):
      syn_sets = wn.synsets(str, pos = wn.NOUN)
      for syn_set in syn_sets:
         nSynList.append(syn_set.lemma_names)

   if('j' in pos):
      syn_sets = wn.synsets(str, pos = wn.ADJ)
      for syn_set in syn_sets:
         adjSynList.append(syn_set.lemma_names)

   if('d' in pos):
      syn_sets = wn.synsets(str, pos = wn.ADV)
      for syn_set in syn_sets:
         advSynList.append(syn_set.lemma_names)

   if not nSynList and not vSynList and not adjSynList and not advSynList:
      return None

   return nSynList, vSynList, adjSynList, advSynList

def formAnnotation (objList, synList):
   obj = ' '.join(objList)
   str = '{'

   for words in range(0, len(synList)):
      if(words == len(synList)-1):
         str += synList[words] + ' : '
      else:
         str += synList[words] + ' - '
   
   str += obj + '}'

   return str
