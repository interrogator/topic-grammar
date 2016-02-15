#!/usr/bin/python

def make_weighted_corpus(testmode = True, maxweight = 4, fastmode = True):
    """
    make newest corpus, attempt 2
    two problems in weighter.py

        1. order in the cycle of iterations is important, when it shouldn't be
        2. infrequent labels don't make it up to the top n keywords for consideration

    to deal with these problems:

        for 1, we keep every function the same weight, except one. once it peaks in importance,
        we store its ideal weight
        for 2, weights don't just increment, they step up and down. this also saves time.

    once the script is done, we take the ideal weights and run that.
    """

    import os, glob, codecs, fileinput, pickle, re
    from contextlib import closing
    from collections import OrderedDict
    from itertools import izip

    labels = ['root', 'nsubj', 'acomp', 'agent', 'amod', 'nsubjpass', 'csubj', 
              'csubjpass', 'dobj', 'ccomp', 'xcomp', 'iobj', 'advcl', 'advmod', 
              'appos', 'acl', 'case', 'compound', 'dative', 'nummod', 'attr', 
              'aux', 'auxpass', 'cc', 'complm', 'conj', 'dep', 'det', 'expl', 
              'hmod', 'hyph', 'infmod', 'intj', 'mark', 'meta', 'neg', 'nmod', 'nn', 
              'npadvmod', 'num', 'number', 'oprd', 'parataxis', 'partmod', 'pcomp', 
              'predet', 'pobj', 'poss', 'possessive', 'preconj', 'prep', 'prt', 
              'punct', 'quantmod', 'relcl']

    # make a list of labels and weights
    lab_scores = []
    for l in labels:
        for i in range(maxweight + 1):
            lab_scores.append((l, i))
    
    # paths to our data
    #dvtst_functions = 'parsed-data/functions-art.dev_test'
    train_functions = 'parsed-data/functions-art.train'
    #dvtst_lemmata = 'parsed-data/lemmata-art.dev_test'
    train_lemmata = 'parsed-data/lemmata-art.train'
    #dvtst_tokens = 'parsed-data/tokens-art.dev_test'
    train_tokens = 'parsed-data/tokens-art.train'
    output_train_name = 'risk.train'
    
    #dev_test = [dvtst_functions, dvtst_lemmata, dvtst_tokens]
    train = [train_functions, train_lemmata, train_tokens]

    baseline = float(codecs.open('baseline.score', 'r', encoding = 'utf-8').read().strip())
    prev_score = float(codecs.open('current.score', 'r', encoding = 'utf-8').read().strip())

    # add previous score to previous iteration
    if os.path.isfile('all.data'):
        data = pickle.load(codecs.open('all.data', 'rb'))
        if len(data[-1]) == 2:
            data[-1].append(prev_score)
        else:
            if len(data) == len(lab_scores):
                print('Apparently done.')
                print(0)
                return

        # if previous iteration was zero and it improved on baseline
        # skip further iterations on that function
        if fastmode:
            if data[-1][1] == 0 and data[-1][2] > baseline:
                for x in range(1, maxweight + 1):
                    if x == 1:
                       scr = baseline
                    else:
                        scr = 0.0
                    data.append([data[-1][0], x, scr])
            if data[-1][1] == 1:
                data.append([data[-1], 1, baseline])
            if data[-1][1] > 1:
                if data[-1][1] <= baseline:
                    for x in range(data[-1][1], maxweight + 1):
                        data.append([data[-1][0], x, 0.0])
    else:
        data = []
    with codecs.open('all.data', 'wb', encoding = 'utf-8') as fo:
        pickle.dump(data, fo)

    # so now, at first iteration, we have []
    # or, at more than one iteration, we have:
    # [[funct, weight, score], ...]

    # now determine new stuff
    iteration = len(data)
    funct, weight = lab_scores[iteration]


    for index, (fline, lline, tline) in enumerate(izip(open(train[0], 'r'), open(train[1], 'r'), open(train[2], 'r'))):
        if index > 99:
            if testmode:
                break
        lline = lline.replace('  ', " , ")
        output_text = ''
        zipped = zip(fline.split(), lline.split(), tline.split())
        for f, l, t in zipped:
            if f == funct:
                score = weight
            else:
                score = 1
            if l == '-PRON-':
                continue
            if l == 'to':
                continue
            if score > 0:
                output_text += (l + ' ') * score

        if not os.path.isfile(output_train_name):
            open(output_train_name, 'w').close()
        with codecs.open(output_train_name, 'a', encoding = 'utf-8') as fo:
            fo.write(output_text.decode('utf-8') + '\n')

    newdata = [funct, weight]
    data.append(newdata)

    with codecs.open('all.data', 'wb', encoding = 'utf-8') as fo:
        pickle.dump(data, fo)
    print( 1 )
    return

if __name__ == '__main__':
    make_weighted_corpus()