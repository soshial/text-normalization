#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
numword for EN_GB
'''

from numword_en import NumWordEN


class NumWordENGB(NumWordEN):
    '''
    NumWord EN_GB
    '''

    def currency(self, val, longval=True):
        '''
        Convert to currency
        '''
        return self._split(val, hightxt=u"pound/s", lowtxt=u"pence",
                                jointxt=u"and", longval=longval)

_NW = NumWordENGB()

def cardinal(value):
    '''
    Convert to cardinal
    '''
    return _NW.cardinal(value)

def ordinal(value):
    '''
    Convert to ordinal
    '''
    return _NW.ordinal(value)

def ordinal_number(value):
    '''
    Convert to ordinal number
    '''
    return _NW.ordinal_number(value)

def currency(value, longval=True):
    '''
    Convert to currency
    '''
    return _NW.currency(value, longval=longval)

def year(value, longval=True):
    '''
    Convert to year
    '''
    return _NW.year(value, longval=longval)

def main():
    '''
    Main
    '''
    for val in [ 1, 11, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 120, 155,
             180, 300, 308, 832, 1000, 1001, 1061, 1100, 1120, 1500, 1701, 1800,
             2000, 2010, 2099, 2171, 3000, 8280, 8291, 150000, 500000, 1000000,
             2000000, 2000001, -21212121211221211111, -2.121212, -1.0000100,
             1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730]:
        _NW.test(val)

if __name__ == "__main__":
    main()
