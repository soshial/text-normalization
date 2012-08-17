# coding: utf-8
"""This script is for testing numword. Please provide 2-letter language code"""
__author__ = 'soshial'
import unittest

class NumwordTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_cardinal(self):
        cardinals = {
            'de':[
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
                [-121211221211111 , u"minus einhunderteinundzwanzig Billionen "
                u"zweihundertelf Milliarden zweihunderteinundzwanzig Millionen "
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
                ],
            'en':[
                [0,u'zero'],
                [4,u'four'],
                [12,u'twelve'],
                [-45,u'minus forty-five'],
                [-2.12,u'minus two point twelve'],
                [-19.98,u'minus nineteen point ninety-eight'],
                [5.980,u'five point ninety-eight'],
                [22000001,u'twenty-two million and one'],
                [399670900,u'three hundred and ninety-nine million, six hundred and seventy thousand, nine hundred'],
                [90311671002,u'ninety billion, three hundred and eleven million, six hundred and seventy-one thousand and two'],
            ],
            'es':[],
            'fr':[],
            'pl':[],
            'ru':[
                [0,u'ноль'],
                [4,u'четыре'],
                [12,u'двенадцать'],
                [21,u'двадцать один'],
                [33,u'тридцать три'],
                [71,u'семьдесят один'],
                [-80,u'минус восемьдесят'],
                [81,u'восемьдесят один'],
                [91,u'девяносто один'],
                [99,u'девяносто девять'],
                [100,u'сто'],
                [101,u'сто один'],
                [102,u'сто два'],
                [113,u'сто тринадцать'],
                [120,u'сто двадцать'],
                [155,u'сто пятьдесят пять'],
                [280,u'двести восемьдесят'],
                [300,u'триста'],
                [308,u'триста восемь'],
                [832,u'восемьсот тридцать два'],
                [1000,u'тысяча'],
                [1001,u'тысяча один'],
                [1065,u'тысяча шестьдесят пять'],
                [1100,u'тысяча сто'],
                [1120,u'тысяча сто двадцать'],
                [1500,u'тысяча пятьсот'],
                [1701,u'тысяча семьсот один'],
                [1800,u'тысяча восемьсот'],
                [2000,u'две тысячи'],
                [2010,u'две тысячи десять'],
                [2099,u'две тысячи девяносто девять'],
                [2171,u'две тысячи сто семьдесят один'],
                [3000,u'три тысячи'],
                [8280,u'восемь тысяч двести восемьдесят'],
                [8291,u'восемь тысяч двести девяносто один'],
                [150000,u'сто пятьдесят тысяч'],
                [220144,u'двести двадцать тысяч сто сорок четыре'],
                [420650,u'четыреста двадцать тысяч шестьсот пятьдесят'],
                [500000,u'пятьсот тысяч'],
                [1000000,u'миллион'],
                [2000000,u'два миллиона'],
                [20000001,u'двадцать миллионов один'],
                [255421650,u'двести пятьдесят пять миллионов четыреста двадцать одна тысяча шестьсот пятьдесят'],
                [399670900,u'триста девяносто девять миллионов шестьсот семьдесят тысяч девятьсот'],
                [90311671002,u'девяносто миллиардов триста одиннадцать миллионов шестьсот семьдесят одна тысяча два'],
#                [10**63,u'вигинтиллион'],
#                [10**81,u'сексвигинтиллион'],
#                [10**99,u'дуотригинтиллион'],
#                [10**108,u'октодециллиард'],
#                [10**144,u'кватторвигинтиллиард'],
#                [10**336,u'ундецицентиллион'],
#                [10**402,u'третригинтацентиллион'],
#                [-21212121211221211111,u'минус двадцать один квинтиллион двести двенадцать квадриллионов сто двадцать один триллион двести одиннадцать миллиардиллионов двести двадцать один миллион двести одиннадцать тысяч сто одиннадцать'],
                [-2.121212,u'минус два целых и двенадцать'],
                [-1.00001,u'минус один целых и ноль'],
            ]
        }
        for number, word in cardinals[language]:
            self.assertEqual(word,numword.cardinal(number))

    def test_ordinal(self):
        ordinals =  {
            'de':[
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
            ],
            'en':[],
            'es':[],
            'fr':[],
            'pl':[],
            'ru':[ # todo implemet inflection testing
                #[256,u"ДВЕСТИ ПЯТЬДЕСЯТ ШЕСТОЙ".lower()],
                #[900,u"ДЕВЯТИСОТЫЙ".lower()],
                #[3000,u"трёхтысячный"],
                #[150000,u"стапятидесятитысячный"],
                #[5000000,u"пятимиллионный"],
                #[51000000,u"пятидесятиодногомиллионный"], # todo 51000000й - как правильно?
                [0,u'нулевого'],
                [1,u'первого'],
                [2,u'второго'],
                [3,u'третьего'],
                [4,u'четвёртого'],
                [5,u'пятого'],
                [6,u'шестого'],
                [7,u'седьмого'],
                [8,u'восьмого'],
                [9,u'девятого'],
                [10,u'десятого'],
                [12,u'двенадцатого'],
                [20,u'двадцатого'],
                [21,u'двадцать первого'],
                [30,u'тридцатого'],
                [31,u'тридцать первого'],
                [33,u'тридцать третьего'],
                [40,u'сорокового'],
                [50,u'пятидесятого'],
                [60,u'шестидесятого'],
                [70,u'семидесятого'],
                [71,u'семьдесят первого'],
                [80,u'восьмидесятого'],
                [81,u'восемьдесят первого'],
                [90,u'девяностого'],
                [91,u'девяносто первого'],
                [99,u'девяносто девятого'],
                [100,u'сотого'],
                [200,u'двухсотого'],
                [300,u'трёхсотого'],
                [400,u'четырёхсотого'],
                [500,u'пятисотого'],
                [600,u'шестисотого'],
                [700,u'семисотого'],
                [800,u'восьмисотого'],
                [900,u'девятисотого'],
                [78,u'семьдесят восьмого'],
                [180,u'сто восьмидесятого'],
                [300,u'трёхсотого'],
                [308,u'триста восьмого'],
                [832,u'восемьсот тридцать второго'],
                [1000,u'тысячного'],
                [1001,u'тысяча первого'],
                [1061,u'тысяча шестьдесят первого'],
                [1100,u'тысяча сотого'],
                [1120,u'тысяча сто двадцатого'],
                [1500,u'тысяча пятисотого'],
                [1701,u'тысяча семьсот первого'],
                [1800,u'тысяча восьмисотого'],
                [1051000000,u'миллиард пятидесятиодногомиллионного'],
                [2000,u'двухтысячного'],
                [2010,u'две тысячи десятого'],
                [2099,u'две тысячи девяносто девятого'],
                [2171,u'две тысячи сто семьдесят первого'],
                [4000,u'четырехтысячного'],
                [8280,u'восемь тысяч двести восьмидесятого'],
                [8291,u'восемь тысяч двести девяносто первого'],
                [150000,u'стапятидесятитысячного'],
                [220144,u'двести двадцать тысяч сто сорок четвёртого'],
                [420650,u'четыреста двадцать тысяч шестьсот пятидесятого'],
                [500000,u'пятисоттысячного'],
                [1000000,u'миллионного'],
                [2000000,u'двухмиллионного'],
                [20000001,u'двадцать миллионов первого'],
                [255421650,u'двести пятьдесят пять миллионов четыреста двадцать одна тысяча шестьсот пятидесятого'],
                [399670900,u'триста девяносто девять миллионов шестьсот семьдесят тысяч девятисотого'],
                [90311671002,u'девяносто миллиардов триста одиннадцать миллионов шестьсот семьдесят одна тысяча второго'],
            ],
        }
        for number, word in ordinals[language]:
            print word," = ",numword.ordinal(number)
            self.assertEqual(word,numword.ordinal(number))

    def test_year(self):
        years = {
            'de':[
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
            ],
            'en':[[0,'zero'],[33,'thirty-three']],
            'es':[],
            'fr':[],
            'pl':[],
            'ru':[],
        }
        for number, word in years[language]:
            self.assertEqual(word,numword.year(number))

    def test_currency(self):
        currencies =  {
            'de':[
                [12222, u"einhundertzweiundzwanzig Euro und zweiundzwanzig Cent"],
                [123322, u"eintausendzweihundertdreiunddreißig Euro und zweiundzwanzig Cent"],
                [686412, u"sechstausendachthundertvierundsechzig Euro und zwölf Cent"],
                [84, u"vierundachtzig Cent"],
                [1, u"ein Cent"],
            ],
            'en':[],
            'es':[],
            'fr':[],
            'pl':[],
            'ru':[],
        }
        for number, word in currencies[language]:
            self.assertEqual(word,numword.currency(number))

if __name__ == '__main__':
    # todo make possible to give the script parameters 'en','de','ru'...
    '''import sys
    arguments = sys.argv
    if len(arguments) < 2: quit("Please specify the language as a parameter!")
    language = arguments[1]'''
    language = 'en'
    if language == 'de': import numword_de as numword
    elif language == 'en': import numword_en as numword
    elif language == 'es': import numword_es as numword
    elif language == 'fr': import numword_fr as numword
    elif language == 'ru': import numword_ru as numword
    elif language == 'pl': import numword_pl as numword
    else: quit("Please specify the language as a parameter!")
    unittest.main()

def simple_manual_test(self, value):
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