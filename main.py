# coding: utf-8
#

def get_canonical_number_from_string(clean_number_string):
    """Converting @str into float or long number"""
    import math,re
    if re.search("[.,]",clean_number_string) and not math.isnan(float(clean_number_string)) and not math.isinf(float(clean_number_string)):
        return float(clean_number_string)
    elif not math.isnan(long(clean_number_string)) and not math.isinf(long(clean_number_string)):
        return long(clean_number_string)
    else:
        raise ValueError

def check_and_convert_into_number(str):
    """This function checks the string for being number and returns spelled numeral in a string"""
    import re
    if not re.search("\d",str): # if numbers are not present then we just return the string back
        return str
    elif re.search("^-?\d+(.|,)?\d*$",str): # canonic number string: '-30.3879'
        clean_number_string = re.sub(',','',str)
    else:
        clean_number_string = re.sub("\D","",str) # just cleaned number: # -30 ,.3879 -> 303879
    try:
        canonical_number = get_canonical_number_from_string(clean_number_string) # cleaned number converting into long/float
    except StandardError:
        logger.info('Problem with processing type of variable (long, float): ' + str + ' -> ' + clean_number_string)
        raise StandardError
    # main processing of the word
    decades = {"'20s":"twenties","1920s":"twenties","'30s":"thirties","1930s":"thirties","'40s":"fourties","1940s":"fourties",
                 "'50s":"fifties","1950s":"fifties","'60s":"sixties","1960s":"sixties","'70s":"seventies","1970s":"seventies",
                 "'80s":"eighties","1980s":"eighties","'90s":"nineties","1990s":"nineties"}
    # todo $¢€£
    if re.search("^-?\d+(.|,)?\d*$",str): return numword_en.cardinal(canonical_number)
    elif re.search("^\d{4}-\d{2,4}$",str): # "1982-(19)95" -> "from 1982 to 1995"
        def daterepl(matchobj):
            try:
                return "from " + numword_en.cardinal(get_canonical_number_from_string(matchobj.group(1))) +" to " + numword_en.cardinal(get_canonical_number_from_string(matchobj.group(2)))
            except StandardError:
                logger.info('Problem with processing type of 2 variables (e.g. 1763-98): ' + str)
                raise StandardError
        return re.sub("(\d{4})-(\d{4})",daterepl,str,0)
    elif re.search("(\d\d\d\d-\d\d-\d\d)|(\d\d-\d\d-\d\d\d\d)|(\d\d\d\d/\d\d/\d\d)|(\d\d/\d\d/\d\d\d\d)",str):
        return ' ' # 2011-10-17, 12/02/1997 are omitted, but the sentences are not
    elif re.search("^(\+?\d?[\(]\d{3}[\)][\.| |\-]?|^\d{3}[\.|\-| ]?)?\d{3}(\.|\-| )?\d\d(\.|\-| )?\d\d$",str):
        print 'phone';return '' # the phone numbers like (607)-432-1000 (916) 934-45-54
    elif re.search("^\d+(-year-old|-pound|-foot|-acre|-year|-liter|-litre|-step|-yard|-day|-hour|-month-old|-month|-million|-week|-mile|-plus|-point|-minute|-inch|-degrees|-second)$",str):
        return re.sub("^\d+",numword_en.cardinal(canonical_number),str)
    elif re.search("^\d+%|‰|‱$",str): # todo per mille, basis point
        return numword_en.ordinal(canonical_number) + ' percent'
    elif re.search("^[\d. -]+$",str): # if we have just clean numbers with math symbols or spaces
        return numword_en.cardinal(canonical_number)
    elif re.search("^\d+(th|rd|nd|st)$",str):
        return numword_en.ordinal(canonical_number)
    elif str in decades:
        return decades[str]
    elif re.search("^\d+k$",str):
        return numword_en.cardinal(canonical_number*1000)
    elif re.search("^\d+m$",str):
        return numword_en.cardinal(canonical_number*1000000)
    else:
        return re.sub("[\d.-]+",numword_en.cardinal(canonical_number),clean_number_string)

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

# initializing logging
import logging
logger = logging.getLogger('norm')
hdlr = logging.FileHandler('./norm.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# initializing database
import MySQLdb
conn = MySQLdb.connect (host = "192.168.2.101",
    user = "builder",
    passwd = "builderpass",
    db = "builder")
cursor = conn.cursor ()

principal_words = {}
other_words = {}
cursor.execute ("SELECT word_id, word_spelling, principal FROM word_equivalents WHERE lang = 'en' AND relation = 1 OR principal > 0")
while True:
    row = cursor.fetchone ()
    if row is None:
        break
    if row[2]: principal_words[int(row[0])] = unicode(row[1]) # {46:'analyzer'}
    else: other_words[unicode(row[1])] = int(row[0]) # {'analyser':46}
logger.info("Equivalent words imported: %d" % cursor.rowcount)

dictionary = set()
cursor.execute ("SELECT word FROM en_us")
while True:
    row = cursor.fetchone ()
    if row is None:
        break
    dictionary.add(row[0])
logger.info("Dictionary entries imported: %d" % cursor.rowcount)
cursor.close ()

conn.close ()


# processing script arguments
import sys
arguments = sys.argv
path_in = arguments[1] # '/home/soshial/text-normalization/in/'
path_out = arguments[2] # '/home/soshial/text-normalization/out/'

# initializing linguistic components
from nltk.tokenize import *
import nltk.data
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
from numword import numword_en
# NB! nltk.download() # для работы программы необходимо при первом запуске раскомментировать строку и скачать модуль punkt tokenizer models # todo add to readme

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
            sentence_out = ''; omit = False
            words = PunktWordTokenizer().tokenize(sentence_in)
            for word in words:
                if re.search("\d",word): # if numbers are not present then we just return the string back
                    try:
                        word = check_and_convert_into_number(word)
                    except StandardError, error_message:
                        omit = True
                        logger.info('Problem with: ' + unicode(error_message) +':  '+ word)
                        continue
                if omit: break; # if something happens while converting, we should omit the sentence
                temp_word = dictionary_check(word)
                sentence_out += temp_word + ' '
            if not omit:
                sentence_out = re.sub(re.compile("[^\w. '-]",re.UNICODE),"",sentence_out) + "\n" # todo \p{L} is not yet supported by Python 2.7.2
                sentence_out = re.sub(" ('s|'ve|'d|'re|'ll|'t)","\\1",sentence_out) # todo make adequate! 's 've 'd should be tokenized with the word
                file_outtxt.write(sentence_out)
        file_outtxt.close()
        os.remove(fullpath_inmeta) # removing ./in/_____.meta for the loop not to process it again
        #os.remove(path_in + filename_intxt) # removing original ./in/_____.txt
        file_meta = codecs.open(path_out + fullpath_inmeta.split('/')[-1], 'w', 'utf-8') # creating ./out/_____.meta
        file_meta.close()
    #time.sleep(wait)


# usual/currency/year/temperature/time

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
