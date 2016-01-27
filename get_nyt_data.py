import os
import re
from bs4 import BeautifulSoup

os.chdir('~/work/risk/data/NYT-parsed')

reg = re.compile(r'Document [0-9]+ of [0-9]+...>')
risk = re.compile(r'(?i)\brisk')
texts = []
if os.path.isfile('risk_data.txt'):
    os.remove('risk_data.txt')
subcorpora = sorted([d for d in os.listdir('.') if os.path.isdir(d)])

def flatten_treestring(tree):
    import re
    tree = re.sub(r'\(.*? ', '', tree).replace(')', '')
    tree = tree.replace('$ ', '$').replace('`` ', '``').replace(' ,', ',').replace(' .', '.').replace("'' ", "''").replace(" n't", "n't").replace(" 're","'re").replace(" 'm","'m").replace(" 's","'s").replace(" 'd","'d").replace(" 'll","'ll").replace('  ', ' ')
    return tree

rdict = {}

from corpkit.process import tregex_engine
for index, subcorpus in enumerate(subcorpora):
    print 'Doing %d/%d: %s' % (index + 1, len(subcorpora), subcorpus)
    result = tregex_engine(corpus = subcorpus, options = ['-t', '-o', '-f'], query = r'ROOT << __', preserve_case = True)
    for fil, data in result:
        if rdict.get(fil, 'no') == 'no':
            rdict[fil] = []
        rdict[fil].append(data)

    # now we have a dict of filename, list of sents

for k, v in rdict.items():
    text = ' '.join(v)
    print os.path.basename(k) + ': ' + text[:100] + '...'
    if text and not text.startswith('Not available') and re.search(risk, text.lower()):
        texts.append(text)
    else:
        if not re.search(risk, text.lower()):
            print 'No risk word!'

data = '\n'.join(texts)
with open('nyt_data.txt', 'w') as fo:
    fo.write(data.encode('utf-8', errors = 'ignore'))


