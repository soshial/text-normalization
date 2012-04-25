# coding: utf-8
__author__ = 'soshial'

def dictionary_check(word):
    """Checks the word and its variations for being in the dictionary"""
    # the function should transform "The orthopaedics's co-ordination of aedicule is well-kno-wn." into "The orthopedics's coordination of edicule is well-known."
    # todo support inflection (pymorphy/hunspell for russian)
    # todo support unambiguous abbreviations unfolding
    # todo Latin words such as 'etc.', 'e.g.' etc. into pronouncible form
    # todo 10 to 13 years -> ten to thirteen year's
    def spelling_variant_check(words):
        """Checks whether any from @words is in our substitution list"""
        for word_variant in words:
            word_variant = word_variant.lower()
            if word_variant in other_words:
                return principal_words[other_words[word_variant]].lower()
        return word
    word = unicode(word)
    if word.upper() in dictionary:
        return spelling_variant_check([word])
    import re
    i = 1
    clean_word = re.sub("\W","",word).upper()
    variants = {clean_word, re.sub("-","",word).upper(), re.sub(" ","",word).upper()} # the list of all variants of the word
        # for example, for the word "file" @variants would be: set(['FIL-E', 'FIL E', 'FI-LE', 'FI LE', 'FILE', 'F-ILE', 'F ILE'])
    for letter in clean_word:
        if i == len(clean_word): break
        variants.add(clean_word[:i] + ' ' + clean_word[i:])
        variants.add(clean_word[:i] + '-' + clean_word[i:])
        #variants.add(clean_word[:i] + '\'' + clean_word[i:])
        i += 1
    entered = False # @entered shows if there is some variant in the @dictionary
    for var in variants & dictionary: # some variant is in dictionary
        entered = True
        if word.lower() == var.lower(): return word
    if not entered: # zero variants are in dictionary
        return spelling_variant_check(variants)
    else:
        return var.lower() # if it had entered the loop, but the original word is not there, then we return one of the variants

# initializing database
def init_dic(lang):
    import MySQLdb
    conn = MySQLdb.connect (host = "192.168.2.101",
        user = "builder",
        passwd = "builderpass",
        db = "builder")
    cursor = conn.cursor ()

    principal_words = {}
    other_words = {}
    cursor.execute ("SET NAMES 'utf8' COLLATE 'utf8_general_ci'")
    cursor.execute ("SELECT word_id, word_spelling, principal FROM word_equivalents_%s WHERE lang = '%s' AND relation = 1 OR principal > 0" % (lang,lang))
    while True:
        row = cursor.fetchone ()
        #quit(row[1])
        if row is None:
            break
        if row[2]: principal_words[int(row[0])] = (row[1]) # {46:'analyzer'}
        else: other_words[(row[1])] = int(row[0]) # {'analyser':46}
    #logger.info("Equivalent words imported: %d" % cursor.rowcount)

    dictionary = set()
    cursor.execute ("SELECT word FROM dict_%s" % lang)
    while True:
        row = cursor.fetchone ()
        if row is None:
            break
        dictionary.add(row[0])
    #logger.info("Dictionary entries imported: %d" % cursor.rowcount)
    cursor.close ()

    conn.close ()
    return dictionary,principal_words,other_words


# processing script arguments
import sys
arguments = sys.argv
lang = arguments[1] # en|ru|fr...
path_in = arguments[2] # '/home/soshial/text-normalization/in/'
path_out = arguments[3] # '/home/soshial/text-normalization/out/'

# initializing logging
import logging
logger = logging.getLogger('norm')
hdlr = logging.FileHandler('./norm.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# initializing linguistic components
# NB! nltk.download() # для работы программы необходимо при первом запуске раскомментировать строку и скачать модуль punkt tokenizer models # todo add to readme
from nltk.tokenize import *
import nltk.data as nltk_data
exec("import num_"+lang+" as num; numw = num.Num"+lang.title()+"(lang,logger)")
sent_detector = nltk_data.load('tokenizers/punkt/english.pickle')
dictionary,principal_words,other_words = init_dic(lang)

# working with files
import glob, os, codecs

import  re#, time
#wait = 0.01
# todo cut in the end of file <span> </>
# main loop
while True:
    for fullpath_inmeta in glob.glob( os.path.join(path_in, '*.meta') ):
        # file_in - input file, file_in2 - copy of input file, file_out - output file
        filename_intxt = fullpath_inmeta.split('/')[-1].split('.')[-2] + '.txt'
        logger.info('processing ' + path_in + filename_intxt)
        file_intxt = codecs.open( path_in + filename_intxt, "r", "utf-8" )
        text_in = file_intxt.read() # variable @file_intxt with our text to process
        file_outtxt = codecs.open(path_out + filename_intxt, 'w', 'utf-8-sig') # output file as ./out/_____.out
        sentences = sent_detector.tokenize(text_in)
        for sentence_in in sentences:
            sentence_out = ''; omit = False; i = 0;
            words = PunktWordTokenizer().tokenize(sentence_in[:-1])
            for word in words:
                if re.search("\d",word): # if numbers are not present then we just return the string back
                    try:
                        if i-1>0 and words[i-1] == "-": word = numw.check_and_convert_into_number("-"+word)
                        else: word = numw.check_and_convert_into_number(word)
                    except StandardError, error_message:
                        omit = True
                        logger.info('Problem with: ' + unicode(error_message) +':  '+ word)
                        continue
                if omit: break; # if something happens while converting, we should omit the sentence
                if re.search(re.compile("\w",re.UNICODE),unicode(word)):
                    temp_word = dictionary_check(word)
                    sentence_out += temp_word + ' '
                i += 1
            if not omit:
                sentence_out = re.sub(re.compile("[^\w. '-]",re.UNICODE),"",sentence_out) # todo \p{L} is not yet supported by Python 2.7.2
                sentence_out = re.sub(" ('s|'ve|'d|'re|'ll|'t)","\\1",sentence_out) # todo make adequate! 's 've 'd should be tokenized with the word
                file_outtxt.write(sentence_out.strip() + "\n")
        file_outtxt.close()
        os.remove(fullpath_inmeta) # removing ./in/_____.meta for the loop not to process it again
        #os.remove(path_in + filename_intxt) # removing original ./in/_____.txt
        file_meta = codecs.open(path_out + fullpath_inmeta.split('/')[-1], 'w', 'utf-8') # creating ./out/_____.meta
        file_meta.close()
    #time.sleep(wait)


#

#tokenization
#nltk.sentence_tokenize
#nltk.word_tokenize

#text case normalization
#text='aiUOd'
#print text.lower()
#print text.upper()

#canonicalization: "co-operation" → "cooperation", "valour" → "valor", "should've" → "should have" / redis?

#punctuation removal
#puncts='.?!'
#for sym in puncts:
#    text= text.replace(sym,' ')

# NER
# tagger = nltk.data.load('chunkers/maxent_ne_chunker/english_ace.pickle')
# tagger.parse([('Guido', 'NNP'), ('lives', 'NNS'), ('in', 'IN'), ('Seattle', 'NNP')] )
# gives: Tree('S', [Tree('NE', [('Guido', 'NNP')]), ('lives', 'NNS'), ('in', 'IN'), Tree('NE', [('Seattle', 'NNP')])])
