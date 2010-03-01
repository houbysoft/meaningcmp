#!/usr/bin/env python
# (c) Jan Dlabal (http://houbysoft.com), 2010.
# provided under the GNU GPL v3 License.

import nltk
from nltk.corpus import wordnet as wn

min_sim = 0.4

def mncmp(s1,s2):
    s1_tokenized = nltk.word_tokenize(s1)
    s2_tokenized = nltk.word_tokenize(s2)
    s2_ssets = [wn.synsets(item) for item in s2_tokenized]
    s1_ssets = [wn.synsets(item) for item in s1_tokenized]
    s1_counter = list(s1_ssets)
    s2_counter = list(s2_ssets)
    if len(s1_ssets) != len(s2_ssets):
        return False
    stop = False
    for item1 in s1_ssets:
        if item1 not in s1_counter:
            continue
        for item2 in s2_ssets:
            if item2 not in s2_counter:
                continue
            for synset1 in item1:
                for synset2 in item2:
                    if wn.path_similarity(synset1,synset2) >= min_sim:
                        s1_counter.remove(item1)
                        s2_counter.remove(item2)
                        stop = True
                        break
                if stop:
                    break
            if stop:
                break
        stop = False
    if len(s1_counter)==0 and len(s2_counter)==0:
        return True
    else:
        return False


