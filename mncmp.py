#!/usr/bin/env python
# (c) Jan Dlabal (http://houbysoft.com), 2010.
# provided under the GNU GPL v3 License.

import nltk
from nltk.corpus import wordnet as wn

min_sim = 0.33

def mncmp(s1,s2):
    s1_tokenized = nltk.word_tokenize(s1)
    s2_tokenized = nltk.word_tokenize(s2)
    s1_postags = nltk.pos_tag(s1_tokenized)
    s2_postags = nltk.pos_tag(s2_tokenized)
    s2_ssets = [wn.synsets(item) or ['!',item] for item in s2_tokenized]
    s1_ssets = [wn.synsets(item) or ['!',item] for item in s1_tokenized]
    s1_counter = list(s1_ssets)
    s2_counter = list(s2_ssets)
    if len(s1_ssets) != len(s2_ssets):
        return False
    stop = False
    for item1 in s1_ssets:
        try:
            if item1 not in s1_counter:
                continue
        except:
            pass
        for item2 in s2_ssets:
            try:
                if item2 not in s2_counter:
                    continue
            except:
                pass
            try:
                if item1[0]=='!' or item2[0]=='!' or s1_postags[s1_ssets.index(item1)][1]=="NNP" or s2_postags[s2_ssets.index(item2)][1]=="NNP": # in this case, we want a perfect match
                    if s1_tokenized[s1_ssets.index(item1)] == s2_tokenized[s2_ssets.index(item2)]:
                        s1_counter.remove(item1)
                        s2_counter.remove(item2)
                        stop = True
                        break
                    else:
                        continue
            except:
                pass
            for synset1 in item1:
                for synset2 in item2:
                    try:
                        if wn.path_similarity(synset1,synset2) >= min_sim:
                            s1_counter.remove(item1)
                            s2_counter.remove(item2)
                            stop = True
                            break
                    except:
                        pass
                if stop:
                    break
            if stop:
                break
        stop = False
    if len(s1_counter)==0 and len(s2_counter)==0:
        return True
    else:
        if len(s1_counter)==len(s2_counter):
            args = []
            for i in range(0,len(s2_counter)):
                try:
                    if s2_counter[i][0]=='!' and s2_counter[i][1][0:3]=='arg':
                        x = int(s2_counter[i][1][3:]) - 1
                        if x + 1 > len(args):
                            for j in range(len(args),x + 1):
                                args.append('')
                        args[x] = s1_tokenized[s1_ssets.index(s1_counter[i])]
                    else:
                        return False
                except:
                    return False
            return args
        return False


