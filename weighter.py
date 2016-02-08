#!/usr/bin/python

def make_weighted_corpus():
    """
    make newest weighted corpus

    workflow:
    1. iterate over dev_test/train
    2. get function/lemma/token info
    3. determine proper weighting from:
        a) previous weighting
        b) success of previous model
    4. duplicate tokens according to weights
    5. output to file, save weights
    """

    import os, glob, codecs, fileinput, json
    from contextlib import closing
    from collections import OrderedDict
    from itertools import izip
    dvtst_functions = 'parsed-data/functions-art.dev_test'
    train_functions = 'parsed-data/functions-art.train'
    dvtst_lemmata = 'parsed-data/lemmata-art.dev_test'
    train_lemmata = 'parsed-data/lemmata-art.train'
    dvtst_tokens = 'parsed-data/tokens-art.dev_test'
    train_tokens = 'parsed-data/tokens-art.train'
    dev_test = [dvtst_functions, dvtst_lemmata, dvtst_tokens]
    train = [train_functions, train_lemmata, train_tokens]

    # find out if first run or not
    first_run = len(glob.glob('to_model/*.weights')) == 0
    if first_run:
        num_prev = 0
    else:
        num_prev = len(glob.glob('to_model/*.weights'))

    # store as ordered dict so we can modify more important things first...
    # we know that root and nsubj have some topic meaning, so we start with those
    # -1 lets us know the value hasn't been modified at all yet

    weights = OrderedDict([
            ["root", 1],
            ["nsubj", 1],
            ["acomp", -1],
            ["advcl", -1],
            ["advmod", -1],
            ["agent", -1],
            ["amod", -1],
            ["appos", -1],
            ["acl", -1],
            ["case", -1],
            ["compound", -1],
            ["dative", -1],
            ["nummod", -1],
            ["attr", -1],
            ["aux", -1],
            ["auxpass", -1],
            ["cc", -1],
            ["ccomp", -1],
            ["complm", -1],
            ["conj", -1],
            ["csubj", -1],
            ["csubjpass", -1],
            ["dep", -1],
            ["det", -1],
            ["dobj", -1],
            ["expl", -1],
            ["hmod", -1],
            ["hyph", -1],
            ["infmod", -1],
            ["intj", -1],
            ["iobj", -1],
            ["mark", -1],
            ["meta", -1],
            ["neg", -1],
            ["nmod", -1],
            ["nn", -1],
            ["npadvmod", -1],
            ["nsubjpass", -1],
            ["num", -1],
            ["number", -1],
            ["oprd", -1],
            ["parataxis", -1],
            ["partmod", -1],
            ["pcomp", -1],
            ["predet", -1],
            ["pobj", -1],
            ["poss", -1],
            ["possessive", -1],
            ["preconj", -1],
            ["prep", -1],
            ["prt", -1],
            ["punct", -1],
            ["quantmod", -1],
            ["punct", -1],
            ["relcl", -1],
            ["xcomp", -1]])

    def get_weights():
        """
        1. access a file containing the previous weights
        2. access bool value for whether the previous topic model is the best yet
        3. adjust weights
        """
        import json
        import os
        from collections import OrderedDict
        if first_run:
            data = weights
        else:
            fs = sorted(glob.glob('to_model/*.weights'))
            print fs[-1]
            data = json.load(codecs.open(fs[-1], 'rb'), object_pairs_hook=OrderedDict)
        return data

    def previous_model_best():
        """
        assess if the previous model was the best one
    
        random right now. raphael needs to add this bit.
        """
        import random
        return bool(random.getrandbits(1))

    def determine_new_weighting(old_weights, latest_model_best):
        """
        output the new set of weights for this run
        """
        from collections import OrderedDict
        new_weights = OrderedDict(old_weights)
        if first_run:
            new_weights = weights
        else:
            last_modified = [k for k, v in old_weights.items() if v > 0][-1]
            if latest_model_best:
                new_weights[last_modified] = new_weights[last_modified] + 1
            else:
                new_weights[last_modified] = new_weights[last_modified] - 1
                try:
                    nextmod = next(k for k, v in old_weights.items() if v < 0)
                except StopIteration:
                    # this should mean we're done
                    return
                new_weights[nextmod] = 1
        return new_weights

    def filenamer():
        """return the output filenames"""
        import os, glob
        if not first_run:
            fnums = [int(os.path.splitext(os.path.basename(f))[0]) \
                  for f in glob.glob('to_model/*')]
            newnum = str(max(fnums) + 1)
        else:
            newnum = '0'
        return '%s.train' % newnum.zfill(4), '%s.dev_test' % newnum.zfill(4), '%s.weights' % (newnum.zfill(4))

    # make some sequential output names
    output_train_name, output_dt_name, output_weight_file = filenamer()
    # get old weights
    old_weights = get_weights()
    # find out if prev model was better
    latest_model_best = previous_model_best()
    # get new weights
    new_weights = determine_new_weighting(old_weights, latest_model_best)

    if not new_weights:
        print('Apparently finished. All functions have been weighted.')
        return

    #print(output_train_name)
    #print(output_dt_name)
    #print(output_weight_file)
    #print(old_weights)
    #print(latest_model_best)
    #print(new_weights)

    for index, (fline, lline, tline) in enumerate(izip(open(dev_test[0], 'r'), open(dev_test[1], 'r'), open(dev_test[2], 'r'))):
        if index > 9:
            break
        print('Doing dev test, iter %d, article %d' % (num_prev, index + 1))
        #print(fline[:25], lline[:25], tline[:25])
        output_text = ''
        zipped = zip(fline.split(), lline.split(), tline.split())
        for f, l, t in zipped:
            score = new_weights.get(f, False)
            if score is False:
                print('NOT FOUND:', f, l, t)
                score = 0
            if l == '-PRON-':
                l = t
            if score > 0:
                output_text += (l + ' ') * score

        if not os.path.isfile(os.path.join('to_model', output_dt_name)):
            open(os.path.join('to_model', output_dt_name), 'w').close()
        with codecs.open(os.path.join('to_model', output_dt_name), 'a', encoding = 'utf-8') as fo:
            fo.write(output_text + '\n')

    for index, (fline, lline, tline) in enumerate(izip(open(train[0], 'r'), open(train[1], 'r'), open(train[2], 'r'))):
        #if index > 9:
        #    break
        print('Doing train, iter %d, article %d' % (num_prev, index + 1))
        output_text = ''
        zipped = zip(fline.split(), lline.split(), tline.split())
        for f, l, t in zipped:
            score = new_weights.get(f, False)
            if score is False:
                print('NOT FOUND:', f, l, t)
                score = 0
            if l == '-PRON-':
                l = t
            if score > 0:
                output_text += (l + ' ') * score

        if not os.path.isfile(os.path.join('to_model', output_train_name)):
            open(os.path.join('to_model', output_train_name), 'w').close()
        with codecs.open(os.path.join('to_model', output_train_name), 'a', encoding = 'utf-8') as fo:
            fo.write(output_text + '\n')

    with codecs.open(os.path.join('to_model', output_weight_file), 'wb', encoding = 'utf-8') as fo:
        json.dump(new_weights, fo)

if __name__ == '__main__':
    make_weighted_corpus()