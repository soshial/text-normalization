#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
"""
numword for EN
"""

from numword_eu import NumWordEU


class NumWordEN(NumWordEU):
    """
    NumWord EN
    """

    def _set_high_numwords(self, high):
        """
        Set high num words
        """
        max_val = 3 + 3 * len(high)
        for word, i in zip(high, range(max_val, 3, -3)):
            self.cards[10**i] = word + u"illion"

    def _setup(self):
        """
        Setup
        """
        self.negword = u"minus "
        self.pointword = u"point"
        self.errmsg_nonnum = "Only numbers may be converted to words."
        self.exclude_title = [u"and", u"point", u"minus"]

        self.mid_numwords = [(1000, u"thousand"), (100, u"hundred"),
                (90, u"ninety"), (80, u"eighty"), (70, u"seventy"),
                (60, u"sixty"), (50, u"fifty"), (40, u"forty"), (30, u"thirty")]
        self.low_numwords = [u"twenty", u"nineteen", u"eighteen", u"seventeen",
                u"sixteen", u"fifteen", u"fourteen", u"thirteen", u"twelve",
                u"eleven", u"ten", u"nine", u"eight", u"seven", u"six", u"five",
                u"four", u"three", u"two", u"one", u"zero"]
        self.ords = {
                u"one": u"first",
                u"two": u"second",
                u"three": u"third",
                u"five": u"fifth",
                u"eight": u"eighth",
                u"nine": u"ninth",
                u"twelve": u"twelfth",
                }


    def _merge(self, curr, next):
        """
        Merge
        """
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1 and nnum < 100:
            return next
        elif 100 > cnum > nnum :
            return (u"%s-%s" % (ctext, ntext), cnum + nnum)
        elif cnum >= 100 > nnum:
            return (u"%s and %s" % (ctext, ntext), cnum + nnum)
        elif nnum > cnum:
            return (u"%s %s" % (ctext, ntext), cnum * nnum)
        return (u"%s, %s" % (ctext, ntext), cnum + nnum)


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
        return self._split(val, hightxt=u"dollar/s", lowtxt=u"cent/s",
                                jointxt=u"and", longval=longval)


_NW = NumWordEN()

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
    # todo "1982-95" -> "from 1982 to 1995"
    # todo 4%
    # todo "13-year-olds"
    for val in [ 1998, 11, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 120, 155,
             180, 300, 308, 832, 1000, 1001, 1061, 1100, 1120, 1500, 1701, 1800,
             2000, 2010, 2099, 2171, 3000, 8280, 8291, 150000, 500000, 1000000,
             2000000, 2000001, -21212121211221211111, -2.121212, -1.0000100,
             1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730]:
        _NW.test(val)
        quit()

if __name__ == "__main__":
    main()
