# coding: utf-8
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

"""numword for German language"""

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
                out.append(unicode(self.cardinal(int(digit))))
                number = " ".join(out)
        return number

    def _merge(self, curr, next):
        """
        Merge
        """
        ctext, cnum, ntext, nnum = curr + next
        if cnum == 1:
            if nnum == 100 or nnum == 10**3 :
                return u"ein" + ntext, nnum
            if nnum >= 10**6 and not (nnum % 10**3):
                return u"eine " + ntext.capitalize(), nnum
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
        return unicode(value) + u"te"

    def currency(self, val, longval=True, old=False, hightxt=False, lowtxt=False, space=True):
        """
        Convert to currency
        """
        self.precision = 2
        if old:
            return self._split(val, hightxt=u"Mark", lowtxt=u"Pfennig(e)",
                                split_precision=0,jointxt=u"und",longval=longval)
        curr = super(NumWordDE, self).currency(val, jointxt=u"und", hightxt=u"Euro",
                        lowtxt=u"Cent", longval=longval, space=space)
        return curr.replace(u"eins", u"ein")

    def cardinal(self, value):
        # catch floats and parse decimalplaces
        if isinstance(value, float):
            prefix, suffix = str(value).split(".")
            pre_card = super(NumWordDE, self).cardinal(int(prefix))
            suf_card = self._cardinal_float(float("." + suffix))
            suf_card = suf_card.replace(u"null %s" % _NW.pointword,_NW.pointword)
            cardinal = pre_card + " " + suf_card
            return cardinal
        else:
            return super(NumWordDE, self).cardinal(value)

    def year(self, value, longval=True):
        self._verify_ordinal(value)
        if not (value//100)%10:
            return self.cardinal(value)
        year = self._split(value, hightxt=u"hundert", longval=longval, space=False)
        if not year.count(self.negword) == 0:
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
    pass

if __name__ == "__main__":
    main()

