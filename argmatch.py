#!/usr/bin/env python
# (c) Jan Dlabal (http://houbysoft.com) 2010.
# provided under the GNU GPL v3 License.


import nltk
from nltk.corpus import wordnet as wn


class Model():
    def __init__(self,els):
        self.els = els
        self.args = filter(lambda el : el[0]=='`',els)

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


def compare(a,b):
    return a == b # TODO


def argmatch(model,tomatch_):
    tomatch = list(tomatch_)
    pos = -1
    lastr = False
    for i in range(0,len(tomatch)):
        if model.contains(tomatch[i],pos+1):
            pos += 1
            tomatch[i] = False
            lastr = True
        elif model.contains('`',pos+1) or model.contains('`',pos):
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
    return r
