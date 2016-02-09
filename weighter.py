#!/usr/bin/python

def make_weighted_corpus(testmode = True):
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

    requirements:

    'parsed-data/functions-art.dev_test'
    'parsed-data/functions-art.train'
    'parsed-data/lemmata-art.dev_test'
    'parsed-data/lemmata-art.train'
    'parsed-data/tokens-art.dev_test'
    'parsed-data/tokens-art.train'

    first iteration must have no risk.weights
    non-first iterations must have current.score and best.score

    """

    import os, glob, codecs, fileinput, pickle
    from contextlib import closing
    from collections import OrderedDict
    from itertools import izip

    # paths to our data

    dvtst_functions = 'parsed-data/functions-art.dev_test'
    train_functions = 'parsed-data/functions-art.train'
    dvtst_lemmata = 'parsed-data/lemmata-art.dev_test'
    train_lemmata = 'parsed-data/lemmata-art.train'
    dvtst_tokens = 'parsed-data/tokens-art.dev_test'
    train_tokens = 'parsed-data/tokens-art.train'
    
    try:
        os.remove('risk.dev_test')
        os.remove('risk.train')
    except OSError:
        pass

    dev_test = [dvtst_functions, dvtst_lemmata, dvtst_tokens]
    train = [train_functions, train_lemmata, train_tokens]

    # find out if first run or not
    num_prev = 0
    first_run = True
    data = pickle.load(codecs.open('risk.weights', 'rb'))
    num_prev = len(data)
    if num_prev > 1:
        first_run = False

    #print(first_run, num_prev)

    def previous_model_best():
        """
        assess if the previous model was the best one
        """

        import codecs
        bs = 'best.score'
        cs = 'current.score'

        currscore = float(codecs.open(cs, 'r', encoding = 'utf-8').read().strip())
        if not os.path.isfile(bs):
            with codecs.open(bs, 'w', encoding = 'utf-8') as fo:
                fo.write(str(currscore))
        bestscore = float(codecs.open(bs, 'r', encoding = 'utf-8').read().strip())
        if currscore > bestscore:
            with codecs.open(bs, 'w', encoding = 'utf-8') as fo:
                fo.write(str(currscore))            
        if first_run:
            return True
        else:
            return currscore > bestscore

    # store as ordered dict so we can modify more important things first...
    # we know that root and nsubj have some topic meaning, so we start with those
    # -1 lets us know the value hasn't been modified at all yet

    def get_weights():
        """
        return previous weights
        """
        import pickle
        import os
        from collections import OrderedDict
        data = pickle.load(codecs.open('risk.weights', 'rb'))
        return data[-1]

    def determine_new_weighting(old_weights, latest_model_best):
        """
        output the new set of weights, based on the old and the prev 
        model being better/worse
        """
        from collections import OrderedDict
        new_weights = OrderedDict(old_weights)
        #if first_run:
        #    new_weights = old_weights
        #else:
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

    # make some output names
    output_train_name = 'risk.train'
    output_dt_name = 'risk.dev_test'
    output_weight_file = 'risk.weights'
    # get old weights
    old_weights = get_weights()
    # find out if prev model was better
    latest_model_best = previous_model_best()
    # get new weights
    new_weights = determine_new_weighting(old_weights, latest_model_best)

    if not new_weights:
        print('Apparently finished. All functions have been weighted.')
        return 0

    #print(output_train_name)
    #print(output_dt_name)
    #print(output_weight_file)
    #print(old_weights)
    #print(latest_model_best)
    #print(new_weights)

    # code below repeats itself for dev_test and train
    # the idea is to match up the lemmata, tokens and functions and print the lemma form
    # by the current weight

    for index, (fline, lline, tline) in enumerate(izip(open(dev_test[0], 'r'), open(dev_test[1], 'r'), open(dev_test[2], 'r'))):
        if index > 99:
            if testmode:
                break
        # print('Doing dev test, iter %d, article %d' % (num_prev, index + 1))
        #print(fline[:25], lline[:25], tline[:25])
        output_text = ''
        zipped = zip(fline.split(), lline.split(), tline.split())
        for f, l, t in zipped:
            score = new_weights.get(f, False)
            if score is False:
                print('NOT FOUND:', f, l, t)
                score = 0
            # what should we do with pronouns? right now, print their actual written form
            if l == '-PRON-':
                l = t
            if score > 0:
                output_text += (l + ' ') * score

        if not os.path.isfile(output_dt_name):
            open(output_dt_name, 'w').close()
        with codecs.open(output_dt_name, 'a', encoding = 'utf-8') as fo:
            fo.write(output_text.decode('utf-8') + '\n')

    for index, (fline, lline, tline) in enumerate(izip(open(train[0], 'r'), open(train[1], 'r'), open(train[2], 'r'))):
        if index > 99:
            if testmode:
                break
        # print('Doing train, iter %d, article %d' % (num_prev, index + 1))
        output_text = ''
        zipped = zip(fline.split(), lline.split(), tline.split())
        for f, l, t in zipped:
            score = new_weights.get(f, False)
            if score is False:
                #print('NOT FOUND:', f, l, t)
                score = 0
            if l == '-PRON-':
                l = t
            if score > 0:
                output_text += (l + ' ') * score

        if not os.path.isfile(output_train_name):
            open(output_train_name, 'w').close()
        with codecs.open(output_train_name, 'a', encoding = 'utf-8') as fo:
            fo.write(output_text.decode('utf-8') + '\n')

    weight_data = pickle.load(codecs.open('risk.weights', 'rb'))
    weight_data.append(new_weights)

    with codecs.open(output_weight_file, 'wb', encoding = 'utf-8') as fo:
        pickle.dump(weight_data, fo)
    return 1

if __name__ == '__main__':
    make_weighted_corpus()
