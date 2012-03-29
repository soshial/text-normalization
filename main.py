# coding: utf-8

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
    clean_number_string = re.sub("[^\d.-]","",str) # cleaned number with minus, dots etc: # -30 ,.3879 -> -30.3879
    try:
        canonical_number = get_canonical_number_from_string(clean_number_string) # cleaned number converting into long/float
    except StandardError:
        logger.info('Problem with processing type of variable (long, float): ' + str + ' -> ' + clean_number_string)
        return '' #canonical_number = get_canonical_number_from_string(re.sub("[^\d]","",str))
    # main processing of the word
    try:
        decades = {"'20s":"twenties","1920s":"twenties","'30s":"thirties","1930s":"thirties","'40s":"fourties","1940s":"fourties",
                 "'50s":"fifties","1950s":"fifties","'60s":"sixties","1960s":"sixties","'70s":"seventies","1970s":"seventies",
                 "'80s":"eighties","1980s":"eighties","'90s":"nineties","1990s":"nineties"}
        if re.search("^\d{4}-\d{2,4}$",str): # "1982-(19)95" -> "from 1982 to 1995"
            def daterepl(matchobj):
                try:
                    return "from " + numword_en.cardinal(get_canonical_number_from_string(matchobj.group(1))) +" to " + numword_en.cardinal(get_canonical_number_from_string(matchobj.group(2)))
                except StandardError:
                    logger.info('Problem with processing type of 2 variables (long, float): ' + str)
                    return ''
            return re.sub("(\d{4})-(\d{4})",daterepl,str,0)
        elif re.search("(\d\d\d\d-\d\d-\d\d)|(\d\d-\d\d-\d\d\d\d)|(\d\d\d\d/\d\d/\d\d)|(\d\d/\d\d/\d\d\d\d)",str):
            return ' ' # 2011-10-17, 12/02/1997 are omitted, but the sentences are not
        elif re.search("^(\+?\d?[\(]\d{3}[\)][\.| |\-]?|^\d{3}[\.|\-| ]?)?\d{3}(\.|\-| )?\d\d(\.|\-| )?\d\d$",str):
            print 'phone';return '' # the phone numbers like (607)-432-1000 (916) 934-45-54
        elif re.search("^\d+(-year-old|-pound|-foot|-acre|-year|-liter|-litre|-step|-yard|-day|-hour|-month-old|-month|-million|-week|-mile|-plus|-point|-minute|-inch|-degrees|-second)$",str): #
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
            return re.sub("[\d.-]+",numword_en.cardinal(canonical_number),str)
    except StandardError, error_message: # todo test TypeError
        logger.info('Problem with handling type of number: ' + unicode(error_message) +'___'+ str + ' -> ' + clean_number_string)
        return ''

def dictionary_check(word):
    """Checks the word and its variations for being in the dictionary"""
    # todo support hunspell
    import re
    i = 1
    variants = {re.sub("-","",word).upper(), re.sub(" ","",word).upper()}
    for letter in word:
        if i == len(word): break
        variants.add((word[:i] + ' ' + word[i:]).upper())
        variants.add((word[:i] + '-' + word[i:]).upper())
        i += 1
    return (variants & dictionary)[0]

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
cursor.execute ("SELECT word_id, word_spelling, principal FROM word_equivalents WHERE lang = 'en' AND relation = 1 AND principal <> -1")
while True:
    row = cursor.fetchone ()
    if row == None:
        break
    if row[2]: principal_words[int(row[0])] = str(row[1]) # {'advise':'102'}
    else: other_words[str(row[1])] = int(row[0]) # {'102':'advice'}
logger.info("Equivalent words imported: %d" % cursor.rowcount)

dictionary = set()
cursor.execute ("SELECT word FROM en_us")
while True:
    row = cursor.fetchone ()
    if row == None:
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
import nltk, re
from numword import numword_en
# NB! nltk.download() # для работы программы необходимо при первом запуске раскомментировать строку и скачать модуль punkt tokenizer models # todo add to readme

# working with files
import glob, os, codecs

import time
wait = 0.01
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
        sentences = nltk.sent_tokenize(text_in)
        for sentence_in in sentences:
            sentence_out = ''; omit = False
            words = nltk.word_tokenize(sentence_in)
            for word in words:
                temp_word = check_and_convert_into_number(word)
                if temp_word == '':
                    omit = True
                    break # if something happens while converting (returns ''), we should omit the sentence
                else: sentence_out += temp_word + ' '
            if not omit:
                file_outtxt.write(re.sub("[^\w\p{L}. '-]","",sentence_out.encode('utf-8')) + '\n') # todo fix unicode writing into file (now it's substituted with spaces)
        file_outtxt.close()
        os.remove(fullpath_inmeta) # removing ./in/_____.meta for the loop not to process it again
        #os.remove(path_in + filename_intxt) # removing original ./in/_____.txt
        file_meta = codecs.open(path_out + fullpath_inmeta.split('/')[-1], 'w', 'utf-8') # creating ./out/_____.meta
        file_meta.close()
    time.sleep(wait)


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
