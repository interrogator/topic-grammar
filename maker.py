def make_file_for_modelling(input_path, plain = True, weights = False, lemmatise = True,
                            dep_type = 'basic-dependencies', outfile = False, at_least_one = False):
    """
    A function that makes files for topic modelling.

    If plain is true, take XML and output string representation

    If plain is false, use weighting. Default weighting if nothing provided."""
    import os
    # parse the xml
    from corenlp_xml.document import Document

    # a list of paragraphs
    fixed = []
    # files to process
    f_list = []

    def plain_processor(sent, dep_type = False, weights = False):
        """non-weighted processing"""
        output = []
        toks = sent.tokens
        for tok in toks:
            if lemmatise:
                output.append(tok.lemma)
            else:
                output.append(tok.word)
        return ' '.join(output)

    def grammatical_processor(sent, dep_type = False, weights = False):
        """weighted processing"""
        if not weights:
            weights = {
            "nsubj": 8,
            "agent": 8,
            "vmod": 4,
            "predet": 0,
            "nn": 0,
            "acomp": 4,
            "number": 1,
            "possessive": 2,
            "poss": 0,
            "quantmod": 0,
            "rcmod": 0,
            "prepc": 0,
            "prt": 0,
            "npadvmod": 0,
            "tmod": 0,
            "pcomp": 0,
            "preconj": 0,
            "csubj": 9,
            "nsubjpass": 7,
            "csubjpass": 8,
            "dobj": 6,
            "ccomp": 9,
            "xcomp": 9,
            "iobj": 5,
            "nmod": 4,
            "advcl": 2,
            "advmod": 2,
            "neg": 0,
            "vocative": 2,
            "aux": 0,
            "mark": 0,
            "discourse": 0,
            "auxpass": 0,
            "punct": 0,
            "expl": 0,
            "cop": 0,
            "nummod": 0,
            "acl": 4,
            "amod": 3,
            "appos": 0,
            "det": 0,
            "neg": 0,
            "compound": 0,
            "mwe": 0,
            "goeswith": 0,
            "name": 7,
            "foreign": 0,
            "conj": 0,
            "cc": 0,
            "punct": 0,
            "case": 0,
            "list": 0,
            "parataxis": 0,
            "remnant": 0,
            "prep": 0,
            "num": 0,
            "pobj": 3,
            "dislocated": 0,
            "reparandum": 0,
            "root": 10,
            "dep": 0}

        # select dependency grammar with this
        from corpkit.process import get_deps
        output = []
        toks = sent.tokens
        deps = get_deps(sent, dep_type)
        # make sure every word is printed once with this kwarg
        if at_least_one:
            weights = {k: v+1 for k, v in weights.items()}
        for tok in toks:
            # for tokens with dependents, get the function
            try:
                typ = next(i.type for i in deps.links if i.dependent.idx == tok.id)
            except StopIteration:
                continue
            # if the function, simplified, is in our dict, retrieve weight
            if typ.split(':', 1)[0].split('_', 1)[0] in weights.keys():
                for n in range(weights[typ.split(':', 1)[0].split('_', 1)[0]]):
                    # do lemmatisation or not
                    if lemmatise:
                        output.append(tok.lemma)
                    else:
                        output.append(tok.word)

            else:
                print 'Not in dict: %s' % typ.split(':', 1)[0].split('_', 1)[0]
        # return sentence as tokenised, space-sep string
        return ' '.join(output)

    # pick processor
    if plain:
        processor = plain_processor
    else:
        processor = grammatical_processor

    # allow passing in of files
    if os.path.isfile(input_path):
        f_list.append(input_path)

    # if dir passed in, make file list
    elif os.path.isdir(input_path):
        for root, dirs, fs in os.walk(input_path):
            for f in fs:
                if not os.path.isfile(os.path.join(root, f)):
                    continue
                if not f.endswith('.txt') and not f.endswith('.xml') and not f.endswith('.p'):
                    continue
                f_list.append(os.path.join(root, f))

    # iterate over files
    num_files = len(f_list)
    for index, filepath in enumerate(f_list):
        print 'Doing %d/%s ... (%d%%)' % (index + 1, num_files, index * 100.0 / num_files)
        
        # read the xml
        with open(filepath, "rb") as text:
            data = text.read()
            corenlp_xml = Document(data)
            # get the sentence objects
            sents = corenlp_xml.sentences
            paragraph = []
            # process each sentence, add to paragraph
            for sent in sents:
                fixed_sent = processor(sent, dep_type, weights)
                paragraph.append(fixed_sent)
            # join paragraph as single line---one 'text' for topic model
            fixed.append(' '.join(paragraph))
            if outfile is False:
                print ' '.join(paragraph)

    # if outfile name, send it there, or else to stdout
    if outfile is True:
        outfile = 'output.txt'

    with open(outfile, 'w') as fo:
        as_str = '\n'.join(fixed)
        fo.write(as_str.encode('utf-8'))
    print '\n\nDone!\n\n'

# allow command line usage
if __name__ == "__main__":
    import sys
    args = sys.argv
    for index, arg in enumerate(args):
        if arg == 'false' or arg == 'False':
            args[index] = False
    make_file_for_modelling(*sys.argv[1:])