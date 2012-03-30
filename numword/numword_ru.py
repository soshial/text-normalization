# coding: utf-8
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
"""
numword for RU
"""

from numword_base import NumWordBase


class NumWordRU(NumWordBase):
    """
    NumWord RU
    """

    def __init__(self):
        super(NumWordRU,self).__init__()
        from pymorphy import get_morph
        self.morph = get_morph('./dicts/converted/ru/')
        self.inflection_case = u"рд" # todo add 'жр'
        #word = u'Вася'.upper()
        #print self.morph.get_graminfo(word)[0]
        #print self.morph.inflect_ru(u'БУТЯВКА', u'дт,мн')
        #quit()

    def _set_high_numwords(self, high):
        """
        Set high num words
        """
        max_val = 3 + 3 * len(high)
        for word, i in zip(high, range(max_val, 3, -3)):
            self.cards[10**i] = word + u"иллион"


    def _base_setup(self):
        """Base setup"""
        lows = [u"нон", u"окт", u"септ", u"секст", u"квинт", u"квадр", u"тр",
                u"миллиард", u"м"] # todo поправить миллиард и другие
        units = [u"", u"ун", u"доде", u"тре", u"кваттуор", u"квин", u"се",
                u"септ", u"окто", u"новем"]
        tens = [u"дец", u"вигинт", u"тригинт", u"квагинт", u"квинквагинт",
                u"сексагинт", u"септагинт", u"октогинт", u"нонагинт"]
        self.high_numwords = [u"cent"] + self._gen_high_numwords(units, tens, lows)


    def _setup(self):
        """
        Setup
        """
        self.negword = u"минус "
        self.pointword = u"point"
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
                u"семь": u"седьмой",
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
            # case for number 671000 is 1000 > 671
            #print "merge ne > cu", next_numb, curr_numb
            return u"%s %s" % (' '.join(curr_text.split(' ')[:-1]) + ' ' + self._inflect(curr_numb % 10, curr_text.split(' ')[-1],next), # in Russian only the last digit depends on high numwords
                               self._inflect(next_numb,next_text,curr)), curr_numb * next_numb # we don't need to inflect current because it was or would be already inflected
        else:
            #print "merge_other: ", next_numb, curr_numb
            return u"%s %s" % (curr_text, next_text), curr_numb + next_numb


    def ordinal(self, value):
        """
        Convert to ordinal
        """
        self._verify_ordinal(value)
        outwords = self.cardinal(value).split(" ")
        lastwords = outwords[-1].split("-")
        lastword = lastwords[-1].lower()
        try:
            lastword = self.ords[lastword]
        except KeyError:
            if lastword[-1] == u"y":
                lastword = lastword[:-1] + u"ie"
            lastword += u"th"
        lastwords[-1] = self._title(lastword)
        outwords[-1] = u"-".join(lastwords)
        return " ".join(outwords)


    def ordinal_number(self, value):
        """
        Convert to ordinal num
        """
        self._verify_ordinal(value)
        return u"%s%s" % (value, self.ordinal(value)[-2:])


    def year(self, val, longval=True):
        """Convert number into year"""
        if not (val//100)%10: # years like 1066 or 2011 are treated as cardinal
            return self.cardinal(val)
        elif 1700 <= val <= 2050: # years in these borders are usually spelled without joining words
            return self._split(val, hightxt=u"", jointxt=u"", longval=longval)
        return self._split(val, hightxt=u"hundred", jointxt=u"and", longval=longval)

    def currency(self, val, longval=True):
        """
        Convert to currency
        """
        return self._split(val, hightxt=u"доллар/ов", lowtxt=u"цент/ов",
                                jointxt=u"и", longval=longval)

    def _inflect(self, value, text, secondary):
        if secondary is None:
            return super(NumWordRU,self)._inflect(value, text)
        elif secondary == 0: # initial inflecting of all numbers
            return self.morph.inflect_ru(text.upper(), self.inflection_case).lower()
        #print 'text   ',text
        sec_text, sec_numb = secondary
        gr_gender = {u'мр',u'жр',u'ср'}
        gr_number = {u'ед',u'мн'}
        gr_declin = {u'им',u'рд',u'дт',u'вн',u'тв',u'пр',u'зв',u'пр2',u'рд2'}
        if self.inflection_case == u"им":
            if value < sec_numb:
                # numerals take @gr_gender from thousands, millions etc. (@sec_text)
                intersection = ",".join(list(gr_gender & # here we compute intersection between @gr_gender and set of grammar info of secondary
                                             set(self.morph.get_graminfo(sec_text.upper())[0]['info'].split(',')))) # and return the string again
                if intersection == '':
                    print "### intersection void: ",value,sec_text,"___",self.morph.get_graminfo(sec_text.upper())[0]['info'];quit()
                    return self.morph.inflect_ru(text.upper(),self.morph.get_graminfo(sec_text.upper())[0]['info']).lower()
                else:
                    return self.morph.inflect_ru(text.upper(), intersection).lower()
            else:
                # thousands, millions etc. take @gr_number from numerals
                if 11<= sec_numb % 100 <= 19 or 5 <= sec_numb % 10 or sec_numb % 10 == 0:
                    return self.morph.inflect_ru(text.upper(), u"рд,мн").lower() # [5...9], [11...19], [20,30...] миллион_ов_
                elif sec_numb % 10 == 1:
                    return self.morph.inflect_ru(text.upper(), u"им,ед").lower() # 1 миллион__
                elif 2 <= (sec_numb % 10) <= 4:
                    return self.morph.inflect_ru(text.upper(), u"рд,ед").lower() # 3 миллион_а_
                else: quit('DIEEEE!! #1')

        else:
            #print '@ne-imenit@@'
            print 'value  ', text, value, '\t\t\tsec___', sec_numb
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
                print '__0:',text.upper(), self.inflection_case, self.morph.inflect_ru(text.upper(), self.inflection_case)
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
    '''def check_and_convert_into_number(str):
        #converting @str into float or long number
        import math
        try:
            if re.search("[.,]",str) and not math.isnan(float(str)) or not math.isinf(float(str)):
                return numword_en.cardinal(float(re.sub("[^\d.-]","",str))) # -asg30 ,.3879th -> -30.3879
            elif not math.isnan(long(str)) or not math.isinf(long(str)):
                canonic_number = long(re.sub("[^\d-]","",str)) # -asg30 3879 th -> -303879
            else:
                return False
        except ValueError:
            return False
        if str.endswith(("th","rd","nd","st")):
            result_words = ordinal(canonic_number)
        elif str.endswith(("k")):
            result_words = cardinal(canonic_number*1000)
        elif str.endswith(("m")):
            result_words = cardinal(canonic_number*1000000)
        else:
            result_words = re.sub("[\d.-]+",cardinal(canonic_number),str)
        return result_words
    import re

    # todo dates "1980s", "'80s" -> eighties
    decades = {"'20s":"twenties","1920s":"twenties","'30s":"thirties","1930s":"thirties","'40s":"fourties","1940s":"fourties",
               "'50s":"fifties","1950s":"fifties","'60s":"sixties","1960s":"sixties","'70s":"seventies","1970s":"seventies",
               "'80s":"eighties","1980s":"eighties","'90s":"nineties","1990s":"nineties"}
    if "1980s" in decades:
        print(decades[str])'''

    for val in [ 255420650,
                  #421650,
     220144,
                 311671000, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 120, 155,
             180, 300, 308, 832, 1000, 1001, 1061, 1100, 1120, 1500, 1701, 1800,
             2000, 2010, 2099, 2171, 3000, 8280, 8291, 150000, 500000, 1000000,
             2000000, 2000001, -21212121211221211111, -2.121212, -1.0000100,
             1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730]:
        _NW.test(val)
        quit()

if __name__ == "__main__":
    main()
