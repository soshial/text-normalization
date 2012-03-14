#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
numword base
'''

from orderedmapping import OrderedMapping


class NumWordBase(object):
    '''
    NumWordBase
    '''

    def __init__(self):
        self.cards = OrderedMapping()
        self.is_title = False
        self.precision = 2
        self.exclude_title = []
        self.negword = u"(-) "
        self.pointword = u"(.)"
        self.errmsg_nonnum = u"type(%s) not in [long, int, float]"
        self.errmsg_floatord = u"Cannot treat float %s as ordinal."
        self.errmsg_negord = u"Cannot treat negative num %s as ordinal."
        self.errmsg_toobig = u"abs(%s) must be less than %s."

        self.high_numwords = None
        self.mid_numwords = None
        self.low_numwords = None
        self.ords = None

        self._base_setup()
        self._setup()
        self._set_numwords()

        self.maxval = 1000 * self.cards.order[0]

    def _base_setup(self):
        '''
        Base Setup
        '''
        pass

    def _setup(self):
        '''
        Setup
        '''
        pass

    def _set_numwords(self):
        '''
        Set num words
        '''
        self._set_high_numwords(self.high_numwords)
        self._set_mid_numwords(self.mid_numwords)
        self._set_low_numwords(self.low_numwords)

    def _set_high_numwords(self, high):
        '''
        Set high num words
        '''
        pass

    def _set_mid_numwords(self, mid):
        '''
        Set mid num words
        '''
        for key, val in mid:
            self.cards[key] = val

    def _set_low_numwords(self, low):
        '''
        Set low num words
        '''
        for word, i in zip(low, range(len(low) - 1, -1, -1)):
            self.cards[i] = word

    @staticmethod
    def _gen_high_numwords(units, tens, lows):
        '''
        Generate high num words
        '''
        out = [u + t for t in tens for u in units]
        out.reverse()
        return out + lows

    def _splitnum(self, value):
        '''
        Split num
        '''
        for elem in self.cards:
            if elem > value:
                continue
            out = []
            if value == 0:
                div, mod = 1, 0
            else:
                div, mod = divmod(value, elem)

            if div == 1:
                out.append((self.cards[1], 1))
            else:
                if div == value:  # The system tallies, eg Roman Numerals
                    return [(div * self.cards[elem], div * elem)]
                out.append(self._splitnum(div))

            out.append((self.cards[elem], elem))

            if mod:
                out.append(self._splitnum(mod))
            return out

    def _merge(self, curr, next):
        '''
        Merge
        '''
        raise NotImplementedError

    def _clean(self, val):
        '''
        Clean
        '''
        out = val
        while len(val) != 1:
            out = []
            curr, next = val[:2]
            if isinstance(curr, tuple) and isinstance(next, tuple):
                out.append(self._merge(curr, next))
                if val[2:]:
                    out.append(val[2:])
            else:
                for elem in val:
                    if isinstance(elem, list):
                        if len(elem) == 1:
                            out.append(elem[0])
                        else:
                            out.append(self._clean(elem))
                    else:
                        out.append(elem)
            val = out
        return out[0]

    def _title(self, value):
        '''
        Return title
        '''
        if self.is_title:
            out = []
            value = value.split()
            for word in value:
                if word in self.exclude_title:
                    out.append(word)
                else:
                    out.append(word[0].upper() + word[1:])
            value = " ".join(out)
        return value

    def _verify_ordinal(self, value):
        '''
        Verify ordinal
        '''
        if not value == long(value):
            raise TypeError, self.errmsg_floatord % (value)
        if not abs(value) == value:
            raise TypeError, self.errmsg_negord % (value)

    def _verify_num(self, value):
        '''
        Verify num
        '''
        return 1

    def _set_wordnums(self):
        '''
        Set word nums
        '''
        pass

    def _cardinal_float(self, value):
        '''
        Convert float to cardinal
        '''
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
            out.append(str(self.cardinal(decimal)))

        return " ".join(out)

    def cardinal(self, value):
        '''
        Convert long to cardinal
        '''
        try:
            assert long(value) == value
        except (ValueError, TypeError, AssertionError):
            return self._cardinal_float(value)

        self._verify_num(value)

        out = ""
        if value < 0:
            value = abs(value)
            out = self.negword

        if value >= self.maxval:
            raise OverflowError(self.errmsg_toobig % (value, self.maxval))

        val = self._splitnum(value)
        words, _ = self._clean(val)
        return self._title(out + words)

    def ordinal(self, value):
        '''
        Convert to ordinal
        '''
        return self.cardinal(value)

    def ordinal_number(self, value):
        '''
        Convert to ordinal number
        '''
        return value

    def _inflect(self, value, text):
        '''
        Inflect
        '''
        text = text.split("/")
        if value == 1:
            return text[0]
        return "".join(text)

    def _split(self, val, hightxt="", lowtxt="", jointxt="",
                    precision=2, longval=True, space=True):
        '''
        Split
        '''
        out = []
        try:
            high, low = val
        except TypeError:
            high, low = divmod(val, (10**precision))
            #high = int(val)
            #low = int(round((val - high) * (10**precision)))
        if high:
            hightxt = self._title(self._inflect(high, hightxt))
            out.append(self.cardinal(high))
            if low:
                if longval:
                    if hightxt:
                        out.append(hightxt)
                    if jointxt:
                        out.append(self._title(jointxt))
            elif hightxt:
                out.append(hightxt)
        if low:
            out.append(self.cardinal(low))
            if lowtxt and longval:
                out.append(self._title(self._inflect(low, lowtxt)))
        if space:
            return " ".join(out)
        else:
            return "".join(out)

    def year(self, value, **kwargs):
        '''
        Convert to year
        '''
        return self.cardinal(value)

    def currency(self, value, **kwargs):
        '''
        Convert to currency
        '''
        return self.cardinal(value)

    def test(self, value):
        '''
        Test
        '''
        try:
            _card = self.cardinal(value)
        except:
            _card = u"invalid"
        try:
            _ord = self.ordinal(value)
        except:
            _ord = u"invalid"
        try:
            _ordnum = self.ordinal_number(value)
        except:
            _ordnum = u"invalid"
        try:
            _curr = self.currency(value)
        except:
            _curr = u"invalid"
        try:
            _year = self.year(value)
        except:
            _year = u"invalid"
        print (u"For %s, cardinal is %s;\n" \
                "\tordinal is %s;\n" \
                "\tordinal number is %s;\n" \
                "\tcurrency is %s;\n" \
                "\tyear is %s." %
                    (value, _card, _ord, _ordnum, _curr, _year))
