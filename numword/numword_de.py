# -*- coding: utf-8 -*-
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
"""
numword for DE
"""
from numword_eu import NumWordEU

#//TODO: Use German error messages
class NumWordDE(NumWordEU):
    """
    NumWord DE
    """
    def _set_high_numwords(self, high):
        """
        Set high num words
        """
        max = 3 + 6*len(high)

        for word, n in zip(high, range(max, 3, -6)):
            self.cards[10**n] = word + u"illiarde"
            self.cards[10**(n-3)] = word + u"illion"

    def _setup(self):
        """
        Setup
        """
        self.negword = u"minus "
        self.pointword = u"Komma"
        self.errmsg_nonnum = u"Nur Zahlen koennen in Worte konvertiert werden."
        self.errmsg_toobig = u"Zahl ist zu gross um in Worte konvertiert zu werden."
        self.exclude_title = []
        lows = [u"Non", u"Okt", u"Sept", u"Sext", u"Quint", u"Quadr", u"Tr",
                u"B", u"M"]
        units = [u"", u"Un", u"Do", u"Tre", u"Quattuor", u"Quin", u"Sex",
                u"Septem", u"Okto", u"Novem"]
        tens = [u"Dezi", u"Vigint", u"Trigint", u"Quadragint", u"Quinquagint",
                u"Sexagint", u"Septuagint", u"Oktogint", u"Nonagint"]
        self.high_numwords = [u"zent"] + self._gen_high_numwords(units, tens, lows)
        self.mid_numwords = [(1000, u"tausend"), (100, u"hundert"),
                (90, u"neunzig"), (80, u"achtzig"), (70, u"siebzig"),
                (60, u"sechzig"), (50, u"fünfzig"), (40, u"vierzig"),
                (30, u"dreißig"), (20, u"zwanzig"), (19, u"neunzehn"),
                (18, u"achtzehn"), (17, u"siebzehn"), (16, u"sechzehn"),
                (15, u"fünfzehn"), (14, u"vierzehn"), (13, u"dreizehn"),
                (12, u"zwölf"), (11, u"elf"), (10, u"zehn")]
        self.low_numwords = [u"neun", u"acht", u"sieben", u"sechs", u"fünf",
                u"vier", u"drei", u"zwei", u"eins", u"null"]
        self.ords = {
                u"eins": u"ers",
                u"drei": u"drit",
                u"acht": u"ach",
                u"sieben": u"sieb",
                u"hundert": u"hunderts",
                u"tausend": u"tausends",
                u"million": u"millionens",
                u"ig": u"igs",
                }
        self.ordflag = False

    def _cardinal_float(self, value):
        """
        Convert float to cardinal
        """
        try:
            assert float(value) == value
        except (ValueError, TypeError, AssertionError):
            raise TypeError(self.errmsg_nonnum % value)
        pre = int(round(value))
        post = abs(value - pre)
        out = [self.cardinal(pre)]
        if self.precision:
            out.append(self._title(self.pointword))

            decimal = int(round(post * (10**self.precision)))
            for digit in tuple([x for x in str(decimal)]):
                out.append(str(self.cardinal(int(digit))))
                number = " ".join(out)
        return number

    def _merge(self, curr, next):
        """
        Merge
        """
        ctext, cnum, ntext, nnum = curr + next
        if cnum == 1:
            if nnum == 100 or nnum == 10**3 :
                return (u"ein" + ntext, nnum)
            if nnum >= 10**6 and not (nnum % 10**3):
                return (u"eine " + ntext.capitalize(), nnum)
            return next
        if nnum > cnum:
            if nnum >= 10**6:
                if ntext[-1] == u"e":
                    ntext = ntext[:-1]
                if cnum > 1:
                    ntext += u"en"
                ctext += " "
            val = cnum * nnum
        else:
            if nnum < 10 < cnum < 100:
                if nnum == 1:
                    ntext = u"ein"
                ntext, ctext =  ctext, ntext + u"und"
            elif nnum < 10 < cnum < 1000:
                if nnum == 1:
                    ntext = u"eins"
                ntext, ctext =  ntext, ctext
            if cnum >= 10**6 and nnum <> 0:
                ctext += " "
            val = cnum + nnum

        word = ctext + ntext
        return (word.strip(), val)

    def ordinal(self, value):
        """
        Convert to ordinal
        """
        self._verify_ordinal(value)
        self.ordflag = True
        outword = self.cardinal(value)
        self.ordflag = False
        for key in self.ords:
            if outword.endswith(key):
                outword = outword[:len(outword) - len(key)] + self.ords[key]
                break
        return outword + u"te"

    def ordinal_number(self, value):
        """
        Convert to ordinal number
        """
        self._verify_ordinal(value)
        return str(value) + u"te"

    def currency(self, val, longval=True, old=False, hightxt=False, \
        lowtxt=False, space=True):
        """
        Convert to currency
        """
        if old:
            return self._split(val, hightxt=u"Mark", lowtxt=u"Pfennig(e)",
                                    jointxt=u"und",longval=longval)
        curr = super(NumWordDE, self).currency(val, jointxt=u"und", \
                hightxt=u"Euro", lowtxt=u"Cent", longval=longval, \
                space=space)
        return curr.replace(u"eins", u"ein")

    def cardinal(self, value):
        # catch floats and parse decimalplaces
        if isinstance(value, float):
            prefix, suffix = str(value).split(".")
            pre_card = super(NumWordDE, self).cardinal(int(prefix))
            suf_card = self._cardinal_float(float("." + suffix))
            suf_card = suf_card.replace(u"null %s" % (_NW.pointword),_NW.pointword)
            cardinal = pre_card + " " + suf_card
            return cardinal
        else:
            return super(NumWordDE, self).cardinal(value)

    def year(self, val, longval=True):
        if not (val//100)%10:
            return self.cardinal(val)
        year = self._split(val, hightxt=u"hundert", longval=longval, space=False)
        if year.count(self.negword) != 0:
            year = year.replace(self.negword, "").strip()
            year = year + u" v. Chr."
        return year.replace(u"eins", u"ein")

_NW = NumWordDE()

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
    Convert to ordinal number
    """
    return _NW.ordinal_number(value)

def currency(value, longval=True, old=False):
    """
    Convert to currency
    """
    return _NW.currency(value, longval=longval, old=old)

def year(value):
    """
    Convert to year
    """
    return _NW.year(value)

def main():
    test_cardinals = [
            [-1.0000100, u"minus eins Komma null"],
            [1.11, u"eins Komma eins eins"],
            [1, u"eins"],
            [11, u"elf"],
            [12, u"zwölf"],
            [21, u"einundzwanzig"],
            [29, u"neunundzwanzig"],
            [30, u"dreißig"],
            [31, u"einunddreißig"],
            [33, u"dreiunddreißig"],
            [71, u"einundsiebzig"],
            [80, u"achtzig"],
            [81, u"einundachtzig"],
            [91, u"einundneunzig"],
            [99, u"neunundneunzig"],
            [100, u"einhundert"],
            [101, u"einhunderteins"],
            [102, u"einhundertzwei"],
            [151, u"einhunderteinundfünfzig"],
            [155, u"einhundertfünfundfünfzig"],
            [161, u"einhunderteinundsechzig"],
            [180, u"einhundertachtzig"],
            [300, u"dreihundert"],
            [301, u"dreihunderteins"],
            [308, u"dreihundertacht"],
            [832, u"achthundertzweiunddreißig"],
            [1000, u"eintausend"],
            [1001, u"eintausendeins"],
            [1061, u"eintausendeinundsechzig"],
            [1100, u"eintausendeinhundert"],
            [1111, u"eintausendeinhundertelf"],
            [1500, u"eintausendfünfhundert"],
            [1701, u"eintausendsiebenhunderteins"],
            [3000, u"dreitausend"],
            [8280, u"achttausendzweihundertachtzig"],
            [8291, u"achttausendzweihunderteinundneunzig"],
            [10100, u"zehntausendeinhundert"],
            [10101, u"zehntausendeinhunderteins"],
            [10099, u"zehntausendneunundneunzig"],
            [12000, u"zwölftausend"],
            [150000, u"einhundertfünfzigtausend"],
            [500000, u"fünfhunderttausend"],
            [1000000, u"eine Million"],
            [1000100, u"eine Million einhundert"],
            [1000199, u"eine Million einhundertneunundneunzig"],
            [2000000, u"zwei Millionen"],
            [2000001, u"zwei Millionen eins"],
            [1000000000, u"eine Milliarde"],
            [2147483647, u"zwei Milliarden einhundertsiebenundvierzig"
             u" Millionen vierhundertdreiundachtzigtausend"
             u"sechshundertsiebenundvierzig"],
            [23000000000, u"dreiundzwanzig Milliarden"],
            [126000000000001, u"einhundertsechsundzwanzig Billionen eins"],
            [-121211221211111 , u"minus "\
            u"einhunderteinundzwanzig Billionen "\
            u"zweihundertelf Milliarden zweihunderteinundzwanzig Millionen "\
            u"zweihundertelftausendeinhundertelf"],
            [1000000000000000, u"eine Billiarde"],
            [256000000000000000, u"zweihundertsechsundfünfzig Billiarden"],
            # I know the next is wrong! but what to do?
            [-2.12, u"minus zwei Komma eins zwei"],
            [7401196841564901869874093974498574336000000000, u"sieben Septil"
             u"liarden vierhunderteins Septillionen einhundertsechsundneunzig S"
             u"extilliarden achthunderteinundvierzig Sextillionen fünfhundertvi"
             u"erundsechzig Quintilliarden neunhunderteins Quintillionen achthu"
             u"ndertneunundsechzig Quadrilliarden achthundertvierundsiebzig Qua"
             u"drillionen dreiundneunzig Trilliarden neunhundertvierundsiebzig "
             u"Trillionen vierhundertachtundneunzig Billiarden fünfhundertvieru"
             u"ndsiebzig Billionen dreihundertsechsunddreißig Milliarden"],
            ]
    i = 1
    for number, word in test_cardinals:
        try:
            assert word == cardinal(number)
            i += 1
        except AssertionError:
            print "Failed:'%s' != '%s' != '%s'" % \
                (number, cardinal(number), word)
            raise AssertionError, "At least one test failed!" \
                " (Test no. %s of %s)" % (i, len(test_cardinals))
    print "All %s tests for cardinal numbers successfully passed." \
        % (len(test_cardinals))

    test_years = [
            # Watch out, negative years are broken!
            [0, u"null"],
            [33, u"dreiunddreißig"],
            [150, u"einhundertfünfzig"],
            [160, u"einhundertsechzig"],
            [1130, u"elfhundertdreißig"],
            [1999, u"neunzehnhundertneunundneunzig"],
            [1984, u"neunzehnhundertvierundachtzig"],
            [2000, u"zweitausend"],
            [2001, u"zweitausendeins"],
            [2010, u"zweitausendzehn"],
            [2012, u"zweitausendzwölf"],
    ]
    i = 1
    for number, word in test_years:
        try:
            assert word == year(number)
        except AssertionError:
            print "Failed:'%s' != '%s' != '%s'" % \
                (number, year(number), word)
            raise AssertionError, "At least one test failed!" \
                " (Test no. %s of %s)" % (i, len(test_years))
    print "All %s tests for year numbers successfully passed." \
        % (len(test_years))


    test_currency =  [
            [12222, u"einhundertzweiundzwanzig Euro und zweiundzwanzig Cent"],
            [123322, u"eintausendzweihundertdreiunddreißig Euro und zweiundzwanzig Cent"],
            [686412, u"sechstausendachthundertvierundsechzig Euro und zwölf Cent"],
            [84, u"vierundachtzig Cent"],
            [1, u"ein Cent"],
    ]
    i = 1
    for number, word in test_currency:
        try:
            assert word == currency(number)
        except AssertionError:
            print "Failed:'%s' != '%s' != '%s'" % \
                (number, currency(number), word)
            raise AssertionError, "At least one test failed!" \
                " (Test no. %s of %s)" % (i, len(test_currency))
    print "All %s tests for currency numbers successfully passed." \
        % (len(test_currency))

    test_ordinal =  [
            [1, u"erste"],
            [3, u"dritte"],
            [11, u"elfte"],
            [12, u"zwölfte"],
            [21, u"einundzwanzigste"],
            [29, u"neunundzwanzigste"],
            [30, u"dreißigste"],
            [31, u"einunddreißigste"],
            [33, u"dreiunddreißigste"],
            [71, u"einundsiebzigste"],
            [80, u"achtzigste"],
            [81, u"einundachtzigste"],
            [91, u"einundneunzigste"],
            [99, u"neunundneunzigste"],
            [100, u"einhundertste"],
            [101, u"einhunderterste"],
            [102, u"einhundertzweite"],
            [151, u"einhunderteinundfünfzigste"],
            [155, u"einhundertfünfundfünfzigste"],
            [161, u"einhunderteinundsechzigste"],
            [180, u"einhundertachtzigste"],
            [300, u"dreihundertste"],
            [301, u"dreihunderterste"],
            [308, u"dreihundertachte"],
            [832, u"achthundertzweiunddreißigste"],
            [1000, u"eintausendste"],
            [1001, u"eintausenderste"],
            [1061, u"eintausendeinundsechzigste"],
            [2000001, u"zwei Millionen erste"],
            # The following is broken
            #[1000000000, "eine Milliardeste"],
            [2147483647, u"zwei Milliarden einhundertsiebenundvierzig"
             u" Millionen vierhundertdreiundachtzigtausend"
             u"sechshundertsiebenundvierzigste"],

    ]
    i = 1
    for number, word in test_ordinal:
        try:
            assert word == ordinal(number)
        except AssertionError:
            print "Failed:'%s' != '%s' != '%s'" % \
                (number, ordinal(number), word)
            raise AssertionError, "At least one test failed!" \
                " (Test no. %s of %s)" % (i, len(test_ordinal))
    print "All %s tests for ordinal numbers successfully passed." \
        % (len(test_ordinal))


if __name__ == "__main__":
    main()

