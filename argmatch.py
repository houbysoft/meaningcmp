#!/usr/bin/env python
# (c) Jan Dlabal (http://houbysoft.com) 2010.
# provided under the GNU GPL v3 License.


import nltk
from nltk.corpus import wordnet as wn


class Model():
    def __init__(self,sentence):
        self.els = self.tokenize(sentence)
        self.args = filter(lambda el : el[0]=='`',self.els)

    def getsentence(self):
        return ljoin(self.els)

    def tokenize(self,s):
        return s.split(" ")

    def contains(self,el,relpos):
        if el=='`':
            try:
                return self.els[relpos][0] == '`'
            except IndexError:
                return False
        else:
            try:
                return compare(self.els[relpos],el)
            except IndexError:
                return False


def ljoin(l):
    r = ""
    for x in l:
        if len(r) != 0:
            r += " "
        r += x
    return r


def compare(a,b,min=0.31):
# returns True if a has equal meaning to b, False otherwise
    asyn = wn.synsets(a)
    bsyn = wn.synsets(b)
    if len(asyn) > 0 and len(bsyn) > 0:
        for ax in asyn:
            if len(filter(lambda x : x == True,map(lambda bx : wn.path_similarity(ax,bx) > min, bsyn)))>0:
                return True
        return False
    else:
        return a == b


def argmatch(model,tomatch_):
    tomatch = nltk.word_tokenize(tomatch_)
    pos = -1
    lastr = True
    for i in range(0,len(tomatch)):
        if model.contains(tomatch[i],pos+1):
            pos += 1
            tomatch[i] = False
            lastr = True
        elif model.contains('`',pos+1) or (model.contains('`',pos) and lastr == False):
            if lastr == True:
                pos += 1
                lastr = False
            else:
                lastr = False
        else:
            return False
    r = list(model.args)
    for i in range(0,len(model.args)):
        try:
            while tomatch[0]==False:
                tomatch.pop(0)
        except IndexError:
            return False
        r[i] = [r[i],[]]
        try:
            while tomatch[0]!=False:
                r[i][1].append(tomatch.pop(0))
        except IndexError:
            pass
        r[i][1] = ljoin(r[i][1])
    return r
