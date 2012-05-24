# coding: utf-8
# This file is part of numword.
# The COPYRIGHT file at the top level of this repository contains the full copyright notices and license terms.
# This file also contains some comments that will help you with extending, fixing or just understanding the module

"""numword base class"""

from orderedmapping import OrderedMapping

class NumWordBase(object):
    """
    NumWordBase
    """

    def __init__(self):
        self.cards = OrderedMapping() # ordered list of numeral words
        self.is_title = False
        self.precision = -1
        self.exclude_title = [] # words that should be excluded from making "Title Case" in using _title() function
        self.negword = u"(-) "
        self.pointword = u"(.)"
        self.errmsg_nonnum = u"type(%s) not in [long, int, float]"
        self.errmsg_floatord = u"Cannot treat float %s as ordinal."
        self.errmsg_negord = u"Cannot treat negative number %s as ordinal."
        self.errmsg_toobig = u"abs(%s) must be less than %s."
        self.inflection = None

        self.high_numwords = None # list of words representing powers of 10³ (e.g. thousands, quadrillions etc.); should all be pregenerated in _set_high_numwords()
        self.mid_numwords = None # dictionary of numbers and their respecting numwords
        self.low_numwords = None # list of lowest numwords without omission ascending starting from zero
        self.ords = None # list of exceptions in generation of ordinals in ordinal()

        self._base_setup()
        self._setup()
        self._set_numwords()

        self.maxval = 1000 * self.cards.order[0] # maximum value able to convert

    def _base_setup(self):
        """Base Setup; may be used for doing anything before main setup()"""
        pass

    def _setup(self):
        """Setting up all needed variables like @negword or @pointword"""
        pass

    def _set_numwords(self):
        """
        The function sets word equivalents for numbers: hign, middle and low
        """
        self._set_high_numwords(self.high_numwords)
        self._set_mid_numwords(self.mid_numwords)
        self._set_low_numwords(self.low_numwords)

    def _set_high_numwords(self, high):
        """
        Set high num words
        """
        pass

    def _set_mid_numwords(self, mid):
        """
        Set mid num words
        """
        for key, val in mid:
            self.cards[key] = val

    def _set_low_numwords(self, low):
        """
        Set low num words
        """
        for word, i in zip(low, range(len(low) - 1, -1, -1)):
            self.cards[i] = word

    @staticmethod
    def _gen_high_numwords(units, tens, lows):
        """Generate high num words"""
        out = [u + t for t in tens for u in units]
        out.reverse()
        return out + lows

    def _splitnum(self, value):
        """This function recursively splits number and the result is a nested list of words.
        The structure of the list is [quantity_of_smth,smth,other]. For example, 323 gives [[(u'one', 1), (u'three', 3)], (u'hundred', 100), [(u'one', 1), (u'twenty', 20), [(u'one', 1), (u'three', 3)]]]
        We're walking through @cards until we encounter a number less or equal than @value"""
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
                if div == value:  # TODO understand # The system tallies, e.g. Roman Numerals
                    return [(div * self.cards[elem], div * elem)]
                out.append(self._splitnum(div))

            out.append((self.cards[elem], elem))

            if mod:
                out.append(self._splitnum(mod))
            return out

    def _merge(self, curr, next):
        """This function regulates the rules of how two adjacent tuples are to be merged to become a text
        For example:
            (u'three', 3) and (u'hundred', 100) become (u'three hundred',300)
            (u'one', 1) and (u'twenty', 20) become ('twenty',20)
            (u'three hundred',300) and (u'twenty-three', 23) become (u'three hundred and twenty-three', 323)
            etc.
        """
        raise NotImplementedError

    def _clean(self, value):
        """This function recursively in a loop converts the list @val into string using _merge() defined in corresponding derived class"""
        out = value
        while len(value) != 1: # the loop does
            out = []
            curr, next = value[:2]
            if isinstance(curr, tuple) and isinstance(next, tuple):
                out.append(self._merge(curr, next))
                if value[2:]:
                    out.append(value[2:]) # todo what does this mean?
            else:
                for elem in value:
                    if isinstance(elem, list):
                        if len(elem) == 1:
                            out.append(elem[0])
                        else:
                            out.append(self._clean(elem)) # recursion unfolds all nested lists onto the upper level
                    else:
                        out.append(elem)
            value = out
        return out[0]

    def _title(self, value):
        """Capitalizes the result excluding @self.exclude_title"""
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
        """Verifies numword whether it can be an ordinal or year (not negative, not float)"""
        # todo str or int?
        if not value == long(value):
            raise TypeError, self.errmsg_floatord % (value)
        if not abs(value) == value:
            raise TypeError, self.errmsg_negord % (value)

    def _verify_num(self, value):
        """
        Verifies number
        """
        #TODO number verification
        return 1

    def _set_wordnums(self):
        """
        Set word nums
        """
        pass

    def _cardinal_float(self, value):
        """
        Convert float to cardinal
        """
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
        out = [self.cardinal(long(integer))]
        if not isinstance(self.pointword, list):
            out.append(self._title(self.pointword))
            out.append(unicode(self.cardinal(decimal)))
        else:
            out.append(self._title(self.pointword[0]))
            out.append(unicode(self.cardinal(decimal)))
            ending = math.trunc(math.log(decimal,10))+1 # 925 -> trunc(2.91) + 1 = 3
            out.append(self._title(self.pointword[ending]))
        return out

    def cardinal(self, value):
        """
        Convert long to cardinal
        """
        try:
            assert long(value) == value
        except (ValueError, TypeError, AssertionError):
            return " ".join(self._cardinal_float(value))

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
        """Convert to ordinal"""
        pass

    def ordinal_number(self, value):
        """Convert to ordinal number (5th, 21st etc.)"""
        pass

    def _inflect(self, value, text, secondary = None):
        """
        Inflects the additional words of high and low parts, e.g. dollar(s), cent(s)
        """
        # todo make possible to inflect all the phrase
        text = text.split("/")
        if value == 1:
            return text[0]
        return u"".join(text)

    def _split(self, value, hightxt="", lowtxt="", jointxt="", split_precision=2, longval=True, space=True):
        """This function is for customizing generated strings (e.g. for currency or year)
        Setting @hightxt=u"dollar/s", @lowtxt=u"cent/s", @jointxt=u"and" with @split_precision '2' gives:
            'currency is sixteen dollars and forty-five cents'
        If @split_precision = 0 then only @hightxt stays; not to be confused with @self.precision!
        Be careful with float numbers!"""
        # todo make customizable, allowing _split() for usual cardinal
        out = []
        try:
            high, low = value
        except TypeError:
            if long(value) == value: # val is integer
                high, low = divmod(value, (10**split_precision)); high = long(high)
            else: # val is float!
                print "#"
                if self.precision == -1:
                    high, low = unicode(value).split(".") # -19.98 -> -19
                    high, low = long(high), long(low)
                else:
                    high = long(value) # -19.98 -> -19
                    low = int(round(abs(abs(value) - abs(high)) * (10**self.precision)))
        if high:
            hightxt = self._title(self._inflect(high,hightxt,(self.cardinal(high),high)))
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
                out.append(self._title(self._inflect(low, lowtxt,(self.cardinal(low),low))))
        if space:
            return u" ".join(out)
        else:
            return u"".join(out)

    def year(self, value, **kwargs):
        """
        Convert to year
        """
        return self.cardinal(value)

    def currency(self, value, **kwargs):
        """
        Convert to currency
        """
        # don't forget to make precision 2 in all child classes!
        # and more important: make it again as it was!
        self.precision = 2
        pass

    def test(self,value,make_test_arrays = False):
        """Test function for manual testing in output; very simple"""
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
        print (u"For %s, cardinal is %s;\n\tordinal is %s;\n\tordinal number is %s;\n\tcurrency is %s;\n\tyear is %s." %
                    (value, _card, _ord, _ordnum, _curr, _year))

    def test_array(self):
        """"""
        for val in [-4.121212, -1.0000100,1051000000,
            0, 1, 2,3, 4, 5,6,7,8,9,10,12, 20,21, 30,31, 33,40,50,60, 70,71, 80, 81, 90,91, 99, 100, 200,300,400,500,600,700,800,900,78,
            180, 300, 308, 832, 1000, 1001, 1061, 1100, 1120, 1500, 1701, 1800,
            2000, 2010, 2099, 2171, 4000, 8280, 8291, 150000, 220144, 420650,
            500000, 1000000, 2000000, 20000001, 255421650, 399670900, 90311671002, -21212121211221211111,


            #1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730
        ]:
            print '['+str(val)+',u\''+self.cardinal(val)+'\'],';quit()