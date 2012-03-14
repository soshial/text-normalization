#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
numword
'''
__version__ = '0.4'

import locale as _locale

_MODULES = []
for _loc in [_locale.getlocale(), _locale.getdefaultlocale()]:
    _lang = _loc[0]
    if _lang:
        _lang = _lang.lower()

        _MODULES.append("numword.numword_" + _lang)
        _MODULES.append("numword.numword_" + _lang.split("_")[0])

for _module in _MODULES:
    try:
        nwmod = __import__(_module)
        components = _module.split('.')
        for comp in components[1:]:
            nwmod = getattr(nwmod, comp)
        break
    except ImportError:
        continue

try:
    def cardinal(value):
        '''
        Convert to cardinal
        '''
        return nwmod.cardinal(value)

    def ordinal(value):
        '''
        Convert to ordinal
        '''
        return nwmod.ordinal(value)

    def ordinal_number(value):
        '''
        Convert to ordinal number
        '''
        return nwmod.ordinal_number(value)

    def currency(value, **kwargs):
        '''
        Convert to currency
        '''
        return nwmod.currency(value, **kwargs)

    def year(value, **kwargs):
        '''
        Convert to year
        '''
        return nwmod.year(value, **kwargs)

except NameError:
    raise ImportError("Could not import any of these modules: %s"
                          % (", ".join(_MODULES)))
