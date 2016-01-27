#!/Users/daniel/virtenvs/ssled/bin/python

# this script grabs texts from proquest html files, turns each article into a paragraph,
# and makes a file with each article on a single file.

import os
import re
from bs4 import BeautifulSoup
os.chdir('/Users/daniel/work/tmp/2016/all')
reg = re.compile(r'Document [0-9]+ of [0-9]+...>')
risk = re.compile(r'(?i)\brisk')
# strip bad stuff from start of line
starter = re.compile(r'^([A-Z0-9 -\']{3,100}(;|:|-+) ?|[A-Z ,]{5,} )')
files = []

if os.path.isfile('risk_data.txt'):
    os.remove('risk_data.txt')
for root, dirs, fs in os.walk('.'):
    for f in fs:
        if f.endswith('html'):
            files.append(os.path.join(root, f))
# these words are often in the last paragraph of articles, which is junk
badwords = ['Illustration:', 'ILLUSTRATION', 'Illustration', 'Photo:', 
            'PHOTO', 'Caption:', 'CAPTION', 'People:', 'PEOPLE']
for index, fp in enumerate(files):
    texts = []
    print 'Doing %d/%d: %s' % (index + 1, len(files), fp)
    with open(fp, 'r') as fo:
        data = fo.read()
        each_article = re.split(reg, data)[1:]
        for article in each_article:
            soup = BeautifulSoup(article)
            text = ' '.join(i.strip() for i in soup.body.text.strip('\n ').splitlines()[1:-1] \
                            if not any(badword in i for badword in badwords) and not i.lower().startswith('photo'))
            text = re.sub(starter, '', text)
            text = re.sub(r'\s+', ' ', text)
            print os.path.basename(fp) + ': ' + text[:100].strip() + '...'
            if text and not text.startswith('Not available') and re.search(risk, text.lower()):
                texts.append(text.strip())
            else:
                if not re.search(risk, text.lower()):
                    print 'No risk word!'
    data = '\n'.join(texts)
    with open('risk_data.txt', 'a') as fo:
        fo.write(data.encode('utf-8', errors = 'ignore'))
