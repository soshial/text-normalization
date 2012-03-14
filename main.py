# coding: utf-8
def is_number(s):
    try:
        return float(s)
    except ValueError:
        return False

import nltk, sys
from numword import numword_en

arguments = sys.argv
#nltk.download() # для работы программы необходимо при первом запуске раскомментировать строку и скачать модуль punkt tokenizer models

import os
import glob
  
path_in = arguments[1]# '/home/soshial/text-normalization/in/'
path_out = arguments[2]# '/home/soshial/text-normalization/out/'
while True:
    for fullpath_inmeta in glob.glob( os.path.join(path_in, '*.meta') ):
        # file_in - input file, file_in2 - copy of input file, file_out - output file
        filename_intxt = fullpath_inmeta.split('/')[-1].split('.')[-2] + '.txt'
        with open(path_in + filename_intxt, 'r') as file_intxt: text_in = file_intxt.read() # variable file_in with our text to process
        file_outtxt = open(path_out + filename_intxt, 'w') # output file as ./out/_____.out
        sentences = nltk.sent_tokenize(text_in)
        for sent in sentences:
            words = nltk.word_tokenize(sent)
            print(words)
            for word in words:
                if is_number(word):
                    file_outtxt.write(str(numword_en.cardinal(is_number(word)))+' ')
                else:
                    file_outtxt.write(word+' ')
            file_outtxt.write('\n')
        file_outtxt.close()
        file_in2 = open(path_out + filename_intxt + '.old', 'w') # saving copy as ./out/_____.txt.old
        file_in2.write(text_in) # writing it
        file_in2.close()
        quit()
        print(path_in + filename_intxt)
        quit()
        os.remove(path_in + filename_intxt) # removing ./in/_____.txt
        os.remove(fullpath_inmeta) # removing ./in/_____.meta
        file_meta = open(path_out + fullpath_inmeta.split('/')[-1], 'w') # creating ./out/_____.meta
        file_meta.close()
    print('waiting')


# вырезать \s
# cardinal/ordinal: 1-st 2-nd 3-rd n-th
# 10m, 512k
# usual/currency/year/temperature

#print numword_en.cardinal(2001,True)
#print NumWordEN('done 2367 for 2')#

#tokenization
#nltk.sentence_tokenize
#nltk.word_tokenize

#text case normalization
#text='aiUOd'
#print text.lower()
#print text.upper()

#numbers into words - numword

#canonicalization: "co-operation" → "cooperation", "valour" → "valor", "should've" → "should have" / redis?

#punctuation removal
#puncts='.?!'
#for sym in puncts:
#    text= text.replace(sym,' ')
