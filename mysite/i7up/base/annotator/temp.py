from nltk.corpus import wordnet as wn

def getSenseSimilarity(worda,wordb):
        """
        find similarity betwwn word senses of two words
        """
        wordasynsets = wn.synsets(worda)
        wordbsynsets = wn.synsets(wordb)
        synsetnamea = [wn.synset(str(syns.name)) for syns in wordasynsets]
        synsetnameb = [wn.synset(str(syns.name)) for syns in wordbsynsets]

        bPathNum = 0
        bWupNum = 0
        bPath = []
        bWup = []

        for sseta, ssetb in [(sseta,ssetb) for sseta in synsetnamea\
        for ssetb in synsetnameb]:
                pathsim = sseta.path_similarity(ssetb)
                wupsim = sseta.wup_similarity(ssetb)

                if pathsim != None:
                        if pathsim > bPathNum:
                                bPathNum = pathsim
                                bPath = [sseta.definition, ssetb.definition]
                        if wupsim > bWupNum:
                                bWupNum = wupsim
                                bWup = [sseta.definition, ssetb.definition]

        if bPathNum:
                print '-------------------------'
                print 'path_similarity() results'
                print 'Num: ',bPathNum
                print 'Def A: ', bPath[0]
                print 'Def B: ', bPath[1]
                print '-------------------------'
        if bWupNum:
                print '-------------------------'
                print 'wup_similarity() results'
                print 'Num: ', bWupNum
                print 'Def A: ', bWup[0]
                print 'Def B: ', bWup[1]
                print '-------------------------'

#                        print '----------------------------'
 #                       print "Path Sim Score: ",pathsim
  #                      print "WUP Sim Score: ",wupsim
   #                     print "Def A: ", sseta.definition
    #                    print "Def B: ", ssetb.definition
     #                   print '----------------------------'
