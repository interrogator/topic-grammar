import os
import glob
import codecs
import spacy
import spacy.en
nlp = spacy.en.English(parser=True, tagger=True, entity=False)

try:
    os.makedirs('parsed-data')
except:
    import shutil
    shutil.rmtree('parsed-data')

for f in glob.glob('data/*'):
    if os.path.basename(f).startswith('.'):
        continue
    print f
    base = os.path.basename(f)
    for index, line in enumerate(codecs.open(f, 'r', encoding = 'utf-8')):
        if index > 10:
            break
        print 'Doing %s: %d' % (f, index + 1)
        tokens = ''
        lemmata = ''
        funct = ''
        extra = ''
        doc = nlp(line)
        for tok in doc:
            if tok.lower_.replace(' ', '-').strip('\n').strip() != '':
                tokens += tok.lower_.replace(' ', '-').strip('\n').strip() + ' '
                lemmata += tok.lemma_.lower().replace(' ', '-').strip('\n').strip() + ' '
                funct += tok.dep_.lower().replace(' ', '-').strip('\n').strip() + ' '

        for name, data in [('tokens', tokens),
                           ('lemmata', lemmata),
                           ('functions', funct)]:
            newname = name + '-' + base
            if not os.path.isfile(os.path.join('parsed-data', newname)):
                open(os.path.join('parsed-data', newname), 'w').close()
            with codecs.open(os.path.join('parsed-data', newname), 'a', encoding = 'utf-8') as fo:
                fo.write(data + '\n')