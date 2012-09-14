# coding: utf-8
"""This file is quite vague script (sorry for that!), just an interface for all normalizing techniques,
   programmed in num and numword classes"""
__author__ = 'soshial'

def dictionary_check(word):
    """Checks the word and its variations for being in the dictionary"""
    # the function should transform "The orthopaedics's co-ordination of aedicule is well-kno-wn." into "The orthopedics's coordination of edicule is well-known."
    # todo support unambiguous abbreviations unfolding
    # todo SPELLING VARIANTS support on VADIM side!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # todo Latin words such as 'etc.', 'e.g.' etc. into pronouncible form
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
    clean_word = regex.sub("[^\w'.-]","",word).upper() # just cleant word only with apostrophies, hyphens and dots

    # checking acronyms like "U.S.A."
    if len(word)>2 and ".".join(list(word)) in dictionary: return ".".join(list(word))
    # cheking abbreviations like "Mr., Mrs., Dr., ..."
    if len(word)<5 and not word in dictionary and word+"." in dictionary: return word+"."
    # checking and splitting hyphenized words like "out-of-order"
    dehyphenized_set = set(clean_word.split("-"))
    if len(dehyphenized_set) == len(dehyphenized_set & dictionary): return regex.sub("-"," ",word) # 'out-of-order' -> 'out of order'
    variants = {clean_word, regex.sub("-","",word).upper()} # the set of all variants of the word
    # generating all possible variants; not applicable, imho
    # for example, for the word "file" @variants would be: set(['FIL-E', 'FIL E', 'FI-LE', 'FI LE', 'FILE', 'F-ILE', 'F ILE'])
#    i = 1
#    for letter in clean_word:
#        if i == len(clean_word): break
#        variants.add(clean_word[:i] + ' ' + clean_word[i:])
#        variants.add(clean_word[:i] + '-' + clean_word[i:])
#        variants.add(clean_word[:i] + '\'' + clean_word[i:])
#        i += 1
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
    global config
    import MySQLdb
    conn = MySQLdb.connect (host = config.get('db','host'), user = config.get('db','user'),
                            passwd = config.get('db','passwd'), db = config.get('db','db'))
    cursor = conn.cursor ()

    principal_words = {}
    other_words = {}
    cursor.execute ("SET NAMES 'utf8' COLLATE 'utf8_general_ci'")
    cursor.execute ("SELECT word_id, word_spelling, principal FROM %s_word_equivalents WHERE lang = '%s' AND relation = 1 OR principal > 0 " % (lang,lang))
    while True:
        row = cursor.fetchone ()
        if row is None:
            break
        if row[2]: principal_words[int(row[0])] = (row[1]) # {46:'analyzer'}
        else: other_words[(row[1])] = int(row[0]) # {'analyser':46}
    #logger.info("Equivalent words imported: %d" % cursor.rowcount)

    dictionary = set()
    cursor.execute ("SELECT word FROM %s_dict WHERE state = 0" % lang)
    while True:
        row = cursor.fetchone ()
        if row is None:
            break
        dictionary.add(row[0])
    #logger.info("Dictionary entries imported: %d" % cursor.rowcount)
    cursor.close ()

    conn.close ()
    return dictionary,principal_words,other_words

def omit_brackets(words):
    counter = 0
    if words.count("(") != words.count(")") or words.count("[") != words.count("]") or words.count("{") != words.count("}"):
        return [] # all brackets should be paired
    while '(' in words and ')' in words and counter < 4:
        words = words[:words.index("(")] + words[words.index(")")+1:]
        counter+=1
    while '[' in words and ']' in words and counter < 4:
        words = words[:words.index("[")] + words[words.index("]")+1:]
        counter+=1
    while '{' in words and '}' in words and counter < 4:
        words = words[:words.index("{")] + words[words.index("}")+1:]
        counter+=1
    if counter > 3: words = []
    return words

def restore_apostrophes(words,sentence):
    i=0 # token counter
    pointer,max_pointer = 0,0 # points to the place where the substring is found
    import string
    for word in words:
        if word.startswith("'") and i>0:
            pointer = string.find(sentence,words[i-1]+word,max_pointer)
            if pointer != -1:
                max_pointer = max(max_pointer,pointer)
                words = words[:i-1]+[words[i-1]+word]+words[i+1:]
                i-=1 # we concatenate two neighbour words - hence we need for @i to stay the same
        i+=1
    return words

def split_twodigits(word):
    """splitting two-digit words"""
    numbers = {'decims':['twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety'],'units':['one','two','three','four','five','six','seven','eight','nine']}
    word = unicode(word)
    if re.search(' ',word): # composite word with spaces
        word_ret = ''
        for word_part in word.split(' '): word_ret += split_twodigits(word_part) + ' '
        return word_ret.strip()
    else: # any simple word without spaces
        if not word == '' and re.search('-',word) and\
                word.split('-')[0].lower() in numbers['decims'] and word.split('-')[1].lower() in numbers['units']:
            return ' '.join(word.split('-')) # word with hyphens
        else: return word # word without hyphens

def abridgement_fix(words):
    #print words;quit()
    i=0 # token counter
    days_of_week = {'Mon':'Monday','Tue':'Tuesday','Thu':'Thursday','Fri':'Friday','Sat':'Saturday'}
    months = {'Jan':'January','Feb':'February','Mar':'March','Apr':'April','Jun':'June','Jul':'July','Aug':'August','Sep':'September','Oct':'October','Nov':'November','Dec':'December'}
    array_isdigit = lambda ar: (len(ar) == 1 and ar[0].isdigit()) or (len(ar) > 1 and (ar[0].isdigit() or array_isdigit(ar[1:])))
    for word in words:
        neighbourhood = words[max(0,i-4):min(i+4,len(words))]
        word = split_twodigits(word)
        if (word == "#" or word == u"№") and i+1<len(words) and words[i+1].isdigit():
            words = words[:i]+[word+words[i+1]]+words[i+2:] # merging #1/№3
        # fixing time representation
        if word in ['p.m.','a.m.','P.M.','A.M.','GMT','UTC'] and words[i-1] == "00" and words[i-2]==":" and words[i-3].isdigit():
            words = words[:i-1]+words[i:] # 4:00 a.m. sounds like 4 a.m.
            i-=1
        if word in ['p.m.','a.m.','P.M.','A.M.','GMT','UTC','PM','pm','AM','am'] and re.match("(\d{1,2})\.(\d{2})",words[i-1]):
            matches = re.match("(\d{1,2})\.(\d{2})",words[i-1])
            words = words[:i-1]+[matches.group(1)]+[matches.group(2)]+words[i+1:]
            i+=1
        # expanding months and days of week
        if (word in days_of_week or word.endswith('.') and word[:-1] in days_of_week) and array_isdigit(neighbourhood):
            if word.endswith('.'):words[i] = days_of_week[word[:-1]]
            else: words[i] = days_of_week[word]
        if (word in months or word.endswith('.') and word[:-1] in months) and array_isdigit(neighbourhood):
            if word.endswith('.'): words[i] = months[word[:-1]]
            else: words[i] = months[word]
        i+=1
    #print words; quit()
    return words

def garbage_stats(words):
    digit_num,word_num = 0,0
    for word in words:
        if re.search("\d",word):
            digit_num+=1
        elif re.search(re.compile("\w",re.UNICODE),word):
            word_num+=1
    if word_num == 0: return 1
    return float(digit_num/word_num)

def typographics(sentence):
    sentence = re.sub(re.compile(u"[`’']",re.UNICODE),u"'",sentence)
    sentence = re.sub(re.compile(u"[’‘’„“«»”]",re.UNICODE),u'"',sentence)
    sentence = re.sub(re.compile(u"[‒]",re.UNICODE),u'-',sentence) # figure dash -> ndash
    sentence = re.sub(re.compile(u"[―]",re.UNICODE),u'-',sentence) # horizontal bar -> mdash
    sentence = re.sub(re.compile(u"[−–‐]",re.UNICODE),u'-',sentence) # only minus sign, only hyphen -> common hyphen-minus
    sentence = re.sub(re.compile(u"(\s?\.){3}",re.UNICODE),u'...',sentence) # ellipsis
    return sentence

# processing script arguments
import sys
arguments = sys.argv
lang = arguments[1] # en|ru|fr...
path_in = arguments[2] # '/home/soshial/text-normalization/in/'
path_out = arguments[3] # '/home/soshial/text-normalization/out/'
do_logging = True
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('normalization.cfg')
import re,regex

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
exec("import num_"+lang+" as num; numw = num.Num"+lang.title()+"(lang,logger)") # import num_ru as num; numw = num.NumRu(lang,logger)
sent_detector = nltk_data.load('tokenizers/punkt/english.pickle')
if lang == "en": dictionary,principal_words,other_words = init_dic(lang)

# working with files
import glob, os, codecs, time
#year = False
# main loop
while True:
    if glob.glob( os.path.join(path_in, '*.meta') ) == []: time.sleep(1); print "sleep" # if no files in a folder then sleep for a second
    if os.path.isfile(path_in + "die"): os.remove(path_in + "die"); quit()
    for fullpath_inmeta in glob.glob( os.path.join(path_in, '*.meta') ):
        # file_in - input file, file_in2 - copy of input file, file_out - output file
        filename_intxt = fullpath_inmeta.split('/')[-1].split('.')[-2] + '.txt'
        print "processing",filename_intxt
        logger.info('processing ' + path_in + filename_intxt)
        file_intxt = codecs.open( path_in + filename_intxt, "r", "utf-8" )
        text_in = typographics(file_intxt.read()) # variable @file_intxt with our text to process
        if lang == "ru": # just adding all ru files to the 'file.list' for AOT to process
            file_list = codecs.open(config.get('lms','aot_path') + "ru_file.list", 'w+', 'utf-8-sig')
            file_list.write(filename_intxt+"\n")
            file_list.close()
        file_outtxt = codecs.open(path_out + filename_intxt, 'w', 'utf-8-sig') # output file as ./out/_____.out
        sentences = sent_detector.tokenize(text_in)
        for sentence_in in sentences:
            if do_logging: print sentence_in
            sentence_out = ''; omit = False; i = 0; words = []
            try:
                if re.search(u"[/|]",sentence_in): omit = True
                # omitting the part of phrase that is considered as play/transcripts characters (MICHELE: ...)
                # has : AND start is all upper OR is title AND first character after : is big
                if regex.search(":",sentence_in) and (sentence_in.split(':')[0].isupper() or sentence_in.split(':')[0].istitle()) and sentence_in.split(':')[1].strip()[0].isupper():
                    sentence_in = ':'.join(sentence_in.split(':')[1:])
                if regex.search(u"\p{L}{2,}[\.?!…]\p{L}{2,}",sentence_in):
                    omit = True
                    print "omitted because of the dot!"
                    logger.info('Dot inside the word problem with sentence:\n____'+sentence_in)
                    continue
                words = PunktWordTokenizer().tokenize(sentence_in)
                if words[-1].endswith('.'): words[-1]=words[-1][:-1] # removing dot in the end of the phrase
                words = omit_brackets(words) # we don't need anything placed in brackets - it worsens LM
                words = abridgement_fix(words)
                words = restore_apostrophes(words,sentence_in) # word tokenizer designedly moves apart words with apostrophes inside them - we try fix this
                if len(words) == 0:
                    omit = True
                # garbage concentration
                if garbage_stats(words) > 1/3:
                    omit = True
                    logger.info('Garbage problem with sentence:\n____'+sentence_in)
                    continue
            except Exception,ExText:
                logger.info('Preprocessing exception: '+unicode(ExText))
            for word in words:
                word = word.translate(['|*',''])
                if re.search("\d",word): # if numbers are not present then we just return the string back
                    # getting neighbour words
                    d = 1
                    neighbours_left = words[max(0,i-d):i]
                    neighbours_right = words[i+1:min(i+d,len(words))+1]
                    if i-1>=0 and words[i-1] == "-": word = "-" + word; neighbours_left = words[max(0,i-d-1):i-1] # negative numbers
                    try:
                        word = numw.check_and_convert_into_number(word,{"left":neighbours_left,"right":neighbours_right})
                        if lang == 'en': word = split_twodigits(word)
                        #if lang == 'ru': word = u"* " + word + u" *"
                    except StandardError, error_message:
                        omit = True
                        logger.info('Problem with : ' + unicode(error_message) +' // word: '+ unicode(word))
                        #print "###################################     Hey! Problem with : " + unicode(error_message) +' // word: '+ unicode(word)
                        continue
                if omit: break; # if something happens while converting, we should omit the sentence
                if re.search(re.compile("\w",re.UNICODE),unicode(word)):
                    if lang == 'en': word = dictionary_check(word)
                    #if lang == 'ru' and word in {u'г.',u'Г.',u'гг.',u'ГГ.'}: year = True
                    sentence_out += word.upper() + ' '
                i += 1
            if not omit:
                sentence_out = regex.sub(u"[^\p{L}. *'-]","",sentence_out)
                #if lang == 'ru' and year == True:
                #    sentence_out = regex.sub(u" г\.| Г\.",u" ГОДУ|ГОД|ГОДА|ГОДОМ|ГОДЕ",sentence_out)
                #    sentence_out = regex.sub(u" гг\.| ГГ\.",u" ГОДЫ|ГОДОВ|ЛЕТ|ГОДАМ|ГОДАХ|ГОДАМИ",sentence_out)
                #    year = False
                if do_logging: print sentence_out
                file_outtxt.write(sentence_out.strip() + "\n")
            else:
                if do_logging: print "    missed"
            if do_logging: print
        file_outtxt.close()
        quit()
        os.remove(fullpath_inmeta) # removing ./in/_____.meta for the loop not to process it again
        #os.remove(path_in + filename_intxt) # removing original ./in/_____.txt
        file_meta = codecs.open(path_out + fullpath_inmeta.split('/')[-1], 'w', 'utf-8') # creating ./out/_____.meta
        file_meta.close()

# canonicalization:
# "co-operation" → "cooperation", "valour" → "valor", "should've" → "should have" / redis?
#
# NER
# tagger = nltk.data.load('chunkers/maxent_ne_chunker/english_ace.pickle')
# tagger.parse([('Guido', 'NNP'), ('lives', 'NNS'), ('in', 'IN'), ('Seattle', 'NNP')] )
# gives: Tree('S', [Tree('NE', [('Guido', 'NNP')]), ('lives', 'NNS'), ('in', 'IN'), Tree('NE', [('Seattle', 'NNP')])])
