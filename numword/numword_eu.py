#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
numword for EU
'''

from numword_base import NumWordBase

class NumWordEU(NumWordBase):
    '''
    NumWord EU
    '''

    def _set_high_numwords(self, high):
        '''
        Set high num words
        '''
        max_val = 3 + 6 * len(high)

        for word, i in zip(high, range(max_val, 3, -6)):
            self.cards[10**i] = word + u"illiard"
            self.cards[10**(i-3)] = word + u"illion"

    def _base_setup(self):
        '''
        Base setup
        '''
        lows = [u"non", u"oct", u"sept", u"sext", u"quint", u"quadr", u"tr",
                u"b", u"m"]
        units = [u"", u"un", u"duo", u"tre", u"quattuor", u"quin", u"sex",
                u"sept", u"octo", u"novem"]
        tens = [u"dec", u"vigint", u"trigint", u"quadragint", u"quinquagint",
                u"sexagint", u"septuagint", u"octogint", u"nonagint"]
        self.high_numwords = [u"cent"] + self._gen_high_numwords(units, tens, lows)

    def currency(self, value, longval=True, jointxt=u"", hightxt=u"Euro/s", \
            lowtxt=u"Euro cent/s", space=True):
        '''
        Convert to currency
        '''
        return self._split(value, hightxt=hightxt, lowtxt=lowtxt,
                                jointxt=jointxt, longval=longval, space=space)

    def _merge(self, curr, next):
        '''
        Merge
        '''
        raise NotImplementedError
