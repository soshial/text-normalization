# coding: utf-8

def check_and_convert_into_number(str):
    """This function checks the string for being number and returns spelled numeral in a string"""
    #converting @str into float or long number
    import math, re
    clean_number_string = re.sub("[^\d.-]","",str)
    if not re.search("\d",str):
        return str
    try:
        if re.search("[.,]",str) and not math.isnan(float(clean_number_string)) and not math.isinf(float(clean_number_string)):
            return numword_en.cardinal(float(clean_number_string)) # -asg30 ,.3879th -> -30.3879
        elif not math.isnan(long(clean_number_string)) or not math.isinf(long(clean_number_string)):
            canonic_number = long(clean_number_string) # -asg30 3879 th -> -303879
        else:
            return str
    except ValueError:
        return str
    decades = {"'20s":"twenties","1920s":"twenties","'30s":"thirties","1930s":"thirties","'40s":"fourties","1940s":"fourties",
               "'50s":"fifties","1950s":"fifties","'60s":"sixties","1960s":"sixties","'70s":"seventies","1970s":"seventies",
               "'80s":"eighties","1980s":"eighties","'90s":"nineties","1990s":"nineties"}
    if str in decades:
        result_words = decades[str]
    elif str.endswith(("th","rd","nd","st")):
        result_words = numword_en.ordinal(canonic_number)
    elif str.endswith(("k")):
        result_words = numword_en.cardinal(canonic_number*1000)
    elif str.endswith(("m")):
        result_words = numword_en.cardinal(canonic_number*1000000)
    else:
        result_words = re.sub("[\d.-]+",numword_en.cardinal(canonic_number),str)
    return result_words

# initializing logging todo fix log permissions
import logging
logger = logging.getLogger('norm')
hdlr = logging.FileHandler('./norm.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# initializing database
'''
import MySQLdb
conn = MySQLdb.connect (host = "192.168.2.101",
    user = "builder",
    passwd = "builderpass",
    db = "builder")
cursor = conn.cursor ()
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone ()
print "server version:", row[0]
cursor.close ()
conn.close ()
'''

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
wait = 0.010

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
        for sent in sentences:
            words = nltk.word_tokenize(sent)
            for word in words:
                file_outtxt.write(re.sub("[^\w. '-]","",(check_and_convert_into_number(word)+' ').encode('utf-8'))) # todo fix unicode writing into file (now it's substituted with spaces)
            file_outtxt.write('\n')
        file_outtxt.close()
        file_in2 = codecs.open(path_out + filename_intxt + '.old', 'w', 'utf-8') # saving copy as ./out/_____.txt.old
        file_in2.write(text_in) # writing it
        file_in2.close()
        #os.remove(path_in + filename_intxt) # todo decide where to move the original ./in/_____.txt
        os.remove(fullpath_inmeta) # removing ./in/_____.meta for the loop not to process it again
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

#punctuation removal todo ?
#puncts='.?!'
#for sym in puncts:
#    text= text.replace(sym,' ')
