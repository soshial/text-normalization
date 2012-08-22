# coding: utf-8
__author__ = 'soshial'

import re

class NumBase(object):
    language = None

    def __init__(self,language,logger):
        self.language = language
        # setting right numword classes
        if language == 'de': from numword import numword_de; self.numword = numword_de.NumWordDE()
        elif language == 'en': from numword import numword_en; self.numword = numword_en.NumWordEN()
        elif language == 'es': from numword import numword_es; self.numword = numword_es.NumWordES()
        elif language == 'fr': from numword import numword_fr; self.numword = numword_fr.NumWordFR()
        elif language == 'ru': from numword import numword_ru; self.numword = numword_ru.NumWordRU()
        else: from numword import numword_en as numword

        self.logger = logger
        self.decades = {}
        self.from_to = u"{from}/{to}"
        self.endings = {}
        self.roman_num_map =  [('M', 1000, 3), ('CM', 900, 1), ('D', 500, 1), ('CD', 400, 1),
                               ('C', 100, 3), ('XC', 90, 1), ('L', 50, 1), ('XL', 40, 1),
                               ('X', 10, 3), ('IX', 9, 1), ('V', 5, 1), ('IV', 4, 1), ('I', 1, 3)]
        self.plus = None
        self.degree= None
        self.number= None
        self.months = None

    def get_canonical_number_from_string(self,clean_number_string):
        """Converting @str into float or long number"""
        import math,re
        if re.search("[.,]",clean_number_string) and not math.isnan(float(clean_number_string)) and not math.isinf(float(clean_number_string)):
            return float(clean_number_string)
        elif not math.isnan(long(clean_number_string)) and not math.isinf(long(clean_number_string)):
            return long(clean_number_string)
        else:
            raise ValueError

    def check_and_convert_into_number(self,str,details):
        """This function checks the string for being number and returns spelled numeral in a string"""
        if not re.search("\d",str): # if numbers are not present then we just return the string back
            return str
        elif re.search("^-?\d+(\.|,)?\d*$",str): # if it is a canonic number string: '-30.3879'
            clean_number_string = re.sub(',','',str)
        else: # if it is some garbage
            if re.search("^.?-?\d+(\.|,)?\d*.?$",str): clean_number_string = re.sub("[^\d.-]","",str) # just cleaned number: # -30 ,.3879 -> 303879
            else: clean_number_string = re.sub("\D","",str) # just cleaned number: # -30 ,.3879 -> 303879
        try:
            canonical_number = self.get_canonical_number_from_string(clean_number_string) # cleaned number converting into long/float
        except StandardError:
            self.logger.info('Problem with processing type of variable (long, float): ' + str + ' -> ' + clean_number_string)
            raise StandardError
        # main processing of the word
        # usual/currency/year/temperature/time
        # todo 40-40 - счёт?
        # todo 1700s
        # todo 40x200
        # todo 6’2″
        type = "-"
        if self.language == 'ru':
            gr_case,gr_num,gr_gend,type = self.detect_inflection(details)
            #print "@___слово:",str,repr(details).decode("unicode-escape"),"  // ",repr(gr_case).decode("unicode-escape"),repr(gr_gend).decode("unicode-escape"),repr(gr_num).decode("unicode-escape"),type
            if len(gr_case):
                if type == 'ord':
                    self.numword.inflection_case = gr_case.pop() + u"," + gr_num.pop() + u"," + gr_gend.pop()
                else:
                    self.numword.inflection_case = gr_case.pop()
            else: self.numword.inflection_case = u"им"
            #print self.numword.inflection_case
        if re.search("^\d+$",str): # simplest natural number
            if 1800 < canonical_number < 2000: return self.numword.year(canonical_number) # a year
            elif type == "ord" or self.is_date_near(details):
                return self.numword.ordinal(canonical_number) # the 1 of March -> the first of March
            else: return self.numword.cardinal(canonical_number) # usual number
        elif re.search("^-?\d+(\.|,)?\d*$",str):
            return self.numword.cardinal(canonical_number) # usual number
        elif re.search("^\d{4}-\d{2,4}$",str): # "1982-(19)95" -> "from 1982 to 1995"
            def daterepl(matchobj):
                try:
                    self.from_to.split("/")
                    return self.from_to.split("/")[0] + " " + self.numword.cardinal(self.get_canonical_number_from_string(matchobj.group(1)))\
                           + " " + self.from_to.split("/")[1] + " " + self.numword.cardinal(self.get_canonical_number_from_string(matchobj.group(2)))
                except StandardError:
                    self.logger.info('Problem with processing type of 2 variables (e.g. 1763-98): ' + str)
                    raise StandardError
            return re.sub("(\d{4})-(\d{4})",daterepl,str,0)
        elif re.search("(\d\d\d\d-\d\d-\d\d)|(\d\d-\d\d-\d\d\d\d)|(\d\d\d\d/\d\d/\d\d)|(\d\d/\d\d/\d\d\d\d)",str):
            #print "#1"
            self.logger.info('Omitting dates: ' + str)
            raise StandardError # 2011-10-17, 12/02/1997 are omitted, but the sentences are not
        elif re.search("^(\+?\d?[\(]\d{3}[\)][\.| |\-]?|^\d{3}[\.|\-| ]?)?\d{3}(\.|\-| )?\d\d(\.|\-| )?\d\d$",str):
            #print "#2"
            self.logger.info('Omitting phone number: ' + str)
            raise StandardError # the phone numbers like (607)-432-1000 (916) 934-45-54
        elif str in self.decades:
            #print "#3"
            return self.decades[str]
        elif re.search(u"^[#№]\d+$",str):
            return self.number+" "+self.numword.cardinal(canonical_number)
        elif re.search("^[$¢€£]-?\d+(\.|,)?\d*$",str): # currencies
            return self.numword.currency(canonical_number)
        elif re.search("^[IVXLCM]{2,}$",str): # roman numerals
            #print "#4"
            return self.numword.cardinal(self.roman_to_int(str))
        elif re.search(u"^-?\d+(°|°?C|°?F)$",str): # temperature
            return self.temperature(long(re.sub("[^\d-]","",str)))
        elif re.search("^-?\d+(\.|,)?\d*.$",str):
            #print "#5"
            if str.endswith(u"k"): return self.numword.cardinal(canonical_number*1000)
            elif str.endswith(u"m"): return self.numword.cardinal(canonical_number*1000000)
            # todo if "60s".endswith(u"s"): 60 seconds or sixties
            elif str.endswith(u"%"): return self.percentage(canonical_number)
            elif str.endswith(u"‰"): return self.percentage(canonical_number,1)
            elif str.endswith(u"‱"): return self.percentage(canonical_number,2)
            elif str.endswith(u"+"): return self.plus.split("/")[0] + " " + self.numword.cardinal(canonical_number) + " " + self.plus.split("/")[1]
            elif str.endswith(u"x"): return self.numword.cardinal(canonical_number) + u" times"
            else: return self.numword.cardinal(canonical_number) # should return self.numword.cardinal(self.short_endings(str))
        elif not self.ordinals(str) is False: # 21st, 9th, 1092nd
            #print "#6"
            return self.ordinals(str)
        # todo localization
        elif re.search("^\d+-?("+"|".join(self.endings)+")$",str):
            #print "#7",str
            return self.complex_endings(str,canonical_number)
        elif re.search("^-?[\d. ]+$",str): # if we have just clean numbers with math symbols or spaces
            #print "#8"
            print u"WARNING!!!_with", str
            self.logger.info("WARNING!!!_with", str + clean_number_string)
            return self.numword.cardinal(canonical_number)
        else:
            #print "#9"
            return re.sub("[\d.-]+",self.numword.cardinal(canonical_number),clean_number_string)

    def int_to_roman(self,i):
        result = []
        for numeral, integer, max_count in self.roman_num_map:
            count = int(i / integer)
            result.append(numeral * count)
            i -= integer * count
        return ''.join(result)

    def roman_to_int(self,str):
        i = result = 0
        repeating = []
        for numeral, integer, max_count in self.roman_num_map:
            repeating[numeral] = 0
            while str[i:i + len(numeral)] == numeral:
                result += integer
                repeating[numeral] += 1
                i += len(numeral)
            if repeating[numeral] > max_count: raise StandardError
        return result

    def date(self,str):
        pass

    def phone(self,str):
        pass

    def ordinals(self,str):
        pass

    def percentage(self,str,power=0):
        pass

    def temperature(self,str):
        pass

    def short_endings(self,str):
        return str

    def complex_endings(self,str,number):
        pass

    def detect_inflection(self,details):
        pass

    def is_date_near(self,details):
        pass