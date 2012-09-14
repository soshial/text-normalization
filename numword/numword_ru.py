# coding: utf-8
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

"""numword for Russian language"""

# materials used:
# * http://www.gramota.ru/class/coach/tbgramota/45_110
# * http://www.gramota.ru/spravka/letters/?rub=rubric_92

from numword_base import NumWordBase


class NumWordRU(NumWordBase):
    """NumWord RU"""

    def __init__(self):
        super(NumWordRU,self).__init__()
        # initializing morphology module for inflecting
        from pymorphy import get_morph
        import ConfigParser
        config = ConfigParser.RawConfigParser()
        config.read('normalization.cfg')
        dicts_folder = config.get('lms','dicts')
        import os
        if not os.path.exists(dicts_folder): quit('Please put existing dictionaries into "'+dicts_folder+'" folder!')
        self.morph = get_morph(dicts_folder)
        self.inflection_case = u"им" # todo add gender for the ending of numeral ('жр')

    def _set_high_numwords(self, high):
        """Sets high num words"""
        max_val = 3 + 3 * len(high)
        for word, i in zip(high, range(max_val, 3, -3)):
            if 10**i == 1000000000: self.cards[1000000000] = u"миллиард"; continue
            self.cards[10**i] = word + u"иллион" # Only the short scale of naming numbers is used In Russia


    def _base_setup(self):
        """Base setup"""
        # 10**33..10**6
        lows = [u"нон", u"окт", u"септ", u"секст", u"квинт", u"квадр", u"тр",
                u"б", u"м"] # todo fix ultra-high numwords
        units = [u"", u"ун", u"дуо", u"тре", u"кваттуор", u"квин", u"секс",
                u"септ", u"окто", u"новем"]
        tens = [u"дец", u"вигинт", u"тригинт", u"квагинт", u"квинквагинт",
                u"сексагинт", u"септагинт", u"октогинт", u"нонагинт"]
        self.high_numwords = [u"cent"] + self._gen_high_numwords(units, tens, lows)


    def _setup(self):
        """
        Setup
        """
        self.negword = u"минус "
        self.pointword = [u"целая", u"десятая", u"сотая", u"тысячная"]
        self.errmsg_nonnum = "Only numbers may be converted to words."
        self.exclude_title = [u"and", u"point", u"minus"]

        self.mid_numwords = [(1000, u"тысяча"), (900, u"девятьсот"), (800, u"восемьсот"), (700, u"семьсот"),
                (600, u"шестьсот"), (500, u"пятьсот"), (400, u"четыреста"),(300, u"триста"),(200, u"двести"), (100, u"сто"),
                (90, u"девяносто"), (80, u"восемьдесят"), (70, u"семьдесят"),
                (60, u"шестьдесят"), (50, u"пятьдесят"), (40, u"сорок"), (30, u"тридцать")]
        self.low_numwords = [u"двадцать", u"девятнадцать", u"восемнадцать", u"семнадцать",
                u"шестнадцать", u"пятнадцать", u"четырнадцать", u"тринадцать", u"двенадцать",
                u"одиннадцать", u"десять", u"девять", u"восемь", u"семь", u"шесть", u"пять",
                u"четыре", u"три", u"два", u"один", u"ноль"]
        self.ords = {
                u"ноль": u"нулевой",
                u"один": u"первый",
                u"два": u"второй",
                u"три": u"третий",
                u"четыре": u"четвёртый",
                u"шесть": u"шестой",
                u"семь": u"седьмой",
                u"восемь": u"восьмой",
                u"восемьдесят": u"восьмидесятый",
                u"сорок": u"сороковой",
                u"девяносто": u"девяностый",
                u"сто": u"сотый",
                u"двести": u"двухсотый",
                u"триста": u"трёхсотый",
                u"четыреста": u"четырёхсотый",
                u"восемьсот": u"восьмисотый",
                u"тысяча": u"тысячный",
                }


    def _merge(self, curr, next):
        """
        Merge
        """
        curr_text, curr_numb, next_text, next_numb = curr + next
        if curr_numb == 1 and next_numb < 1000:
            #print "merge 1 _ ne", next
            return self._inflect(next_numb,next_text,0),next_numb # all separate numbers should be inflected from the start, that is all mid and low numwords (such as 7, 10, 300)
        elif 1000 > curr_numb > next_numb:
            #print "merge ne _ cu", next_numb, curr_numb # all merging in within 1000 don't change any grammar propeties of the adjacent words
            #return u"%s %s" % (self._inflect(curr_numb,curr_text,next), next_text), curr_numb + next_numb
            return u"%s %s" % (curr_text, next_text), curr_numb + next_numb
        elif next_numb > curr_numb:
            # case for number '671000': '1000' > '671'
            # todo make without tam-tams
            if len(curr_text.split(' ')) < 2: whitespace = ''
            else: whitespace = ' '

            if curr_numb == 1: # in Russian if it is only a power of 1000, then we don't need to use 'один' here
                return self._inflect(next_numb,next_text,curr), next_numb
            else:
                return u"%s %s" % (' '.join(curr_text.split(' ')[:-1]) + whitespace + self._inflect(curr_numb % 10, curr_text.split(' ')[-1],next), # in Russian only the last digit depends on high numwords
                               self._inflect(next_numb,next_text,curr)), curr_numb * next_numb # we don't need to inflect current because it was or would be already inflected
        else:
            #print "merge_other: ", next_numb, curr_numb
            return u"%s %s" % (curr_text, next_text), curr_numb + next_numb

    def _cardinal_float(self, value):
        # todo сделать так, чтобы сами числительные по родам согласовывались: "две сотых, одна целая"
        try:
            assert float(value) == value
        except (ValueError, TypeError, AssertionError):
            raise TypeError(self.errmsg_nonnum % value)
        import math
        if self.precision == -1:
            integer, decimal = unicode(value).split(".") # -19.98 -> -19
            integer, decimal = long(integer), long(decimal)
        else:
            integer = long(value) # -19.98 -> -19
            decimal = int(round(abs(abs(value) - abs(integer)) * (10**self.precision)))
        out = [self.cardinal(integer)]
        if not self.precision == 0:
            if 11 <= integer % 100 <= 19 or 5 <= integer % 10 or integer % 10 == 0: out.append(self.morph.inflect_ru(self.pointword[0].upper(),u"мн,рд").lower())
            else: out.append(self.morph.inflect_ru(self.pointword[0].upper(),u"ед,жр" + self.inflection_case).lower())
            out.append(unicode(self.cardinal(decimal)))
            ending = math.trunc(math.log(decimal,10))+1 # 925 -> trunc(2.91) + 1 = 3
            if 11 <= decimal % 100 <= 19 or 5 <= decimal % 10 or decimal % 10 == 0: out.append(self.morph.inflect_ru(self.pointword[ending].upper(),u"мн,рд").lower())
            else: out.append(self.morph.inflect_ru(self.pointword[ending].upper(),u"ед,жр" + self.inflection_case).lower())
        return out

    def ordinal(self, value):
        """Convert to ordinal"""
        # first we need the nominativus case
        self._verify_ordinal(value)

        temp_inflection = self.inflection_case
        self.inflection_case = u"им"
        outwords = self.cardinal(value).split(" ")
        self.inflection_case = temp_inflection # we put the needed case back
        lastword = outwords[-1].lower()
        try:
            lastword = self.ords[lastword]
        except KeyError:
            import re
            if lastword[-2:] == u"ть":
                lastword = lastword[:-2] + u"тый"
            elif lastword[-4:] == u"ьсот":
                lastword = lastword[:-4] + u"исотый"
            elif lastword[-6:] == u"ьдесят":
                lastword = lastword[:-6] + u"идесятый"
            elif re.search(u'(иллиона?(ов)?|ллиарда?(ов)?|ысяч(а|и)?)$',lastword):
                wo_zeros = long(re.sub(u"(000)*$","",unicode(value))) # 19 250 000 000 -> 19 250
                first = long(wo_zeros / 1000) # 19
                second = wo_zeros % 1000 # 250
                zeroes = long(value / wo_zeros) # 1 000 000
                lastword = re.sub(u'(иллион|ллиард|ысяч)(ов|а|и)?$',u'\\1ный',lastword)
                if second != 1:
                    outwords2_str = u""
                    temp_inflection = self.inflection_case
                    self.inflection_case = u"им"
                    if first: outwords2_str = self.cardinal(first * zeroes * 1000) + ' '
                    self.inflection_case = temp_inflection # we put the needed case back
                    for sec_part in self.cardinal(second).split(' '):
                        if sec_part.lower() == u"один": outwords2_str += u"одно"; continue # 51 000 -> пятидесятиоднотысячный
                        outwords2_str += self.morph.inflect_ru(sec_part.upper(),u"рд").lower()
                    return outwords2_str + self.morph.inflect_ru(lastword.upper(),self.inflection_case).lower()
        outwords[-1] = self._title(self.morph.inflect_ru(lastword.upper(),self.inflection_case).lower())
        return " ".join(outwords)


    def ordinal_number(self, value):
        """
        Convert to ordinal num
        """
        self._verify_ordinal(value)
        return u"%s%s" % (value, self.ordinal(value)[-2:])


    def year(self, value, longval=True):
        """Convert number into year"""
        self._verify_ordinal(value)
        return self.ordinal(value)

    def currency(self, value, longval=True):
        temp_precision, self.precision = self.precision, 2
        return_var = self._split(value, hightxt=u"доллар", lowtxt=u"цент",
                                split_precision=0, jointxt=u"и", longval=longval)
        self.precision = temp_precision
        return return_var

    def _inflect(self, value, text, secondary):
        # @secondary is another tuple(val,text) to have a grammatical agreement with
        if secondary is None:
            return super(NumWordRU,self)._inflect(value, text)
        elif secondary == 0: # initial inflecting of all numbers
            return self.morph.inflect_ru(text.upper(), self.inflection_case).lower()
        sec_text, sec_numb = secondary
        gr_gender = {u'мр',u'жр',u'ср'}
        gr_number = {u'ед',u'мн'}
        gr_declin = {u'им',u'рд',u'дт',u'вн',u'тв',u'пр',u'зв',u'пр2',u'рд2'}
        if self.inflection_case == u"им" or self.inflection_case == u"вн":
            if value < sec_numb:
                # numerals take @gr_gender from thousands, millions etc. (@sec_text)
                intersection = ",".join(list(gr_gender & # here we compute intersection between @gr_gender and set of grammar info of secondary
                                             set(self.morph.get_graminfo(sec_text.upper())[0]['info'].split(',')))) # and return the string again
                if intersection == '':
                    return self.morph.inflect_ru(text.upper(),self.morph.get_graminfo(sec_text.upper())[0]['info']).lower()
                else:
                    return self.morph.inflect_ru(text.upper(), intersection).lower()
            else:
                # thousands, millions etc. take @gr_number from numerals
                if 11<= sec_numb % 100 <= 19 or 5 <= sec_numb % 10 or sec_numb % 10 == 0:
                    return self.morph.inflect_ru(text.upper(), u"рд,мн").lower() # [5...9], [11...19], [20,30...] миллион_ов_
                elif sec_numb % 10 == 1:
                    return self.morph.inflect_ru(text.upper(), self.inflection_case + u",ед").lower() # 1 миллион__
                elif 2 <= (sec_numb % 10) <= 4:
                    return self.morph.inflect_ru(text.upper(), u"рд,ед").lower() # 3 миллион_а_
                else: quit('DIEEEE!! #1')

        else:
            #print '@ne-imenit@@'
            #print 'value  ', text, value, '\t\t\tsec___', sec_numb
            if False:
                # numerals take @gr_gender from thousands, millions etc. (@sec_text)
                #intersection = ",".join(list(gr_gender & # here we compute intersection between @gr_gender and set of grammar info of secondary
                #                            set(self.morph.get_graminfo(sec_text.upper())[0]['info'].split(',')))) # and return the string again
                #print 'inter',intersection
                #if intersection == '':
                #    print "### intersection void: ",value,sec_text,"___",self.morph.get_graminfo(sec_text.upper())[0]['info'];quit()
                #    return self.morph.inflect_ru(text.upper(),self.inflection_case + self.morph.get_graminfo(sec_text.upper())[0]['info']).lower()

                #else:
                    #print "###res",self.morph.inflect_ru(text.upper(), re.sub(u"(ед)|(мн)","",self.morph.get_graminfo(sec_text.upper())[0]['info'])).lower()
                    #if sec_numb == 1000:
                #print(self.morph.get_graminfo(u'ТРЕМЯ')[0]['info'])
                #quit('!__'+self.morph.inflect_ru(u'ЧЕТЫРЕ', u'пр'))
                return self.morph.inflect_ru(text.upper(), self.inflection_case).lower()# + ',' + intersection).lower()
                #return self.morph.inflect_ru(text.upper(), re.sub(u"(ед)|(мн)","",self.morph.get_graminfo(sec_text.upper())[0]['info'])).lower()
            if value < sec_numb:
                # numerals take @gr_gender from thousands, millions etc. (@sec_text)
                intersection = ",".join(list(gr_gender & # here we compute intersection between @gr_gender and set of grammar info of secondary
                                             set(self.morph.get_graminfo(sec_text.upper())[0]['info'].split(',')))) # and return the string again
                if intersection == '':
                    print "### intersection void: ",value,sec_text,"___",self.morph.get_graminfo(sec_text.upper())[0]['info'];quit()
                    return self.morph.inflect_ru(text.upper(),self.morph.get_graminfo(sec_text.upper())[0]['info']).lower()
                else:
                    return self.morph.inflect_ru(text.upper(), intersection).lower()
                # todo тысяча в творительном падеже склоняется по разному, если существительное и если числительное http://www.gramota.ru/spravka/letters/?rub=rubric_92
                #else: #quit("sec"+str(sec_numb)+self.morph.inflect_ru(text.upper(),self.inflection_case).lower())
                    #quit('DDIEEE!! #2')
                    #return self.morph.inflect_ru(text.upper(),self.inflection_case).lower()
            else: # inflecting high numwords
                if sec_numb % 10 == 1:
                    return self.morph.inflect_ru(text.upper(), self.inflection_case + u",ед").lower()
                else:

                    return self.morph.inflect_ru(text.upper(), self.inflection_case + u",мн").lower()



_NW = NumWordRU()

def cardinal(value):
    """
    Convert to cardinal
    """
    return _NW.cardinal(value)

def ordinal(value):
    """
    Convert to ordinal
    """
    return _NW.ordinal(value)

def ordinal_number(value):
    """
    Convert to ordinal num
    """
    return _NW.ordinal_number(value)

def currency(value, longval=True):
    """
    Convert to currency
    """
    return _NW.currency(value, longval=longval)

def year(value, longval=True):
    """
    Convert to year
    """
    return _NW.year(value, longval=longval)

def main():
    """Main program"""
    _NW.test_array()
    quit()
    for val in [
             0,''' 4, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 120, 155,
             180, 300, 308, 832, 1000, 1001, 1061, 1100, 1120, 1500, 1701, 1800,
             255421650, 420650, 220144, 311671000,2000, 2010, 2099, 2171, 3000, 8280, 8291, 150000, 500000, 1000000,
             2000000, 2000001, -21212121211221211111, -2.121212, -1.0000100,
             1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730''']:
        _NW.test(val,True)
        #quit()

if __name__ == "__main__":
    main()
