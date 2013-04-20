import annotator.a_parser as ap

def test1():
    fmt = ap.parseIntoFormat('There is <n> to <i> but <i>')
    sentence = 'There is nothing to fear but fear itself'
    res = ap.checkMatchFormat(fmt, sentence)

    assert res == ('n', ['nothing'], [['fear'], ['fear', 'itself']])

def test2():
    fmt = ap.parseIntoFormat('<v> is to <i> well')
    sentence = 'To die is to live well'
    res = ap.checkMatchFormat(fmt, sentence)

    assert res == ('v', ['To', 'die'], [['live']])

def test3():
    fmt = ap.parseIntoFormat('The command <...> is equal to <v>')
    sentence = 'The command is equal to nothing'
    res = ap.checkMatchFormat(fmt, sentence)

    assert res == ('v', ['nothing'], [])

def runTests():
    test1()
    test2()
    test3()

runTests()
