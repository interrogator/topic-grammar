def make_file_for_modelling(input_path, plain = True, weights = False, lemmatise = True,
                            dep_type = 'basic-dependencies', outfile = False, at_least_one = False):
    """
    A function that makes files for topic modelling.

    If plain is true, take XML and output string representation"""
    import os
    from corenlp_xml.document import Document

    fixed = []
    f_list = []


    def plain_processor(sent, dep_type = False, weights = False):
        output = []
        toks = sent.tokens
        for tok in toks:
            if lemmatise:
                output.append(tok.lemma)
            else:
                output.append(tok.word)
        return ' '.join(output)

    def grammatical_processor(sent, dep_type = False, weights = False):
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

        from corpkit.process import get_deps
        output = []
        toks = sent.tokens
        deps = get_deps(sent, dep_type)
        if at_least_one:
            weights = {k: v+1 for k, v in weights.items()}
        for tok in toks:
            try:
                typ = next(i.type for i in deps.links if i.dependent.idx == tok.id)
            except StopIteration:
                continue
            if typ.split(':', 1)[0].split('_', 1)[0] in weights.keys():
                for n in range(weights[typ.split(':', 1)[0].split('_', 1)[0]]):
                    if lemmatise:
                        output.append(tok.lemma)
                    else:
                        output.append(tok.word)
            else:
                print 'Not in dict: %s' % typ.split(':', 1)[0].split('_', 1)[0]
        return ' '.join(output)

    if plain:
        processor = plain_processor
    else:
        processor = grammatical_processor


    if os.path.isfile(input_path):
        f_list.append(input_path)


    elif os.path.isdir(input_path):
        for root, dirs, fs in os.walk(input_path):
            for f in fs:
                if not os.path.isfile(os.path.join(root, f)):
                    continue
                if not f.endswith('.txt') and not f.endswith('.xml') and not f.endswith('.p'):
                    continue
                f_list.append(os.path.join(root, f))

    num_files = len(f_list)
    for index, filepath in enumerate(f_list):
        from IPython.display import display, clear_output
        clear_output()
        print 'Doing %d/%s ... (%d%%)' % (index + 1, num_files, index * 100.0 / num_files)
        with open(filepath, "rb") as text:
            data = text.read()
            corenlp_xml = Document(data)
            sents = corenlp_xml.sentences
            paragraph = []
            for sent in sents:
                fixed_sent = processor(sent, dep_type, weights)
                paragraph.append(fixed_sent)
            fixed.append(' '.join(paragraph))

    if not outfile:
        print '\n'.join(fixed)
        return
        outfile = 'output.txt'

    with open(outfile, 'w') as fo:
        as_str = '\n'.join(fixed)
        fo.write(as_str.encode('utf-8'))
    return


#if __name__ == "__main__":
#    import sys
#    args = sys.argv
#    for index, arg in enumerate(args):
#        if arg == 'false' or arg == 'False':
#            args[index] = False
#    make_file_for_modelling(*sys.argv[1:])