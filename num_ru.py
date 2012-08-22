# coding: utf-8
__author__ = 'soshial'

import num_base,re

class NumRu(num_base.NumBase):
    def __init__(self,language,logger):
        def unique(input):
            output = []
            for x in input:
                if x not in output:
                    output.append(x)
            return output
        super(NumRu,self).__init__(language,logger)
        self.decades = {u"00":u"нулевые",10:u"десятые",20:u"двадцатые",30:u"тридцатые",40:u"сороковые",
                     50:u"пятидесятые",60:u"шестидесятые",70:u"семидесятые",
                     80:u"восьмидесятые",90:u"девяностые",}
        self.from_to = u"с/по"
        self.endings = [u"летний",u"килограммовый",u"сантиметровый",u"годовой",u"литровый",u"ярдовый",
                               u"дневный",u"часовой",u"месячный",u"миллионный",u"недельный",u"километровый",
                               u"минутный",u"дюймовый",u"градусовый",u"секундный"]
        self.months = {u'январь',u'февраль',u'март',u'апрель',u'май',u'июнь',u'июль',u'август',u'сентябрь',u'октябрь',u'ноябрь',u'декабрь'}
        self.cases = {u'им',u'рд',u'дт',u'вн',u'тв',u'пр',u'зв',u'дт2',u'рд2'}
        self.numrs = {u'ед',u'мн'}
        self.genders = {u'мр',u'жр',u'ср'}
        self.prepositions = {u"":[u""],}
        new_endings = []
        for ending in self.endings:
            new_endings.append(ending)
            for form in self.numword.morph.decline(ending.upper()): new_endings.append(form['word'].lower())
        self.endings = unique(new_endings)
        #for t in self.numword.morph.get_graminfo(u"СТОЛОВАЯ".upper()):
        #    if t['class']==u"С": print t['info']#.find(u"жр")
        #quit()
        self.plus = u"более/"
        self.degree = u"градус"
        self.number = u"номер"
        self.numword.morph.inflection_case = u"им"

    def ordinals(self,str):
        # documentation: http://www.gramota.ru/spravka/letters/?rub=rubric_99
        if re.search(u"^\d+-?(й|го|му|м|е|я|ю|х|ми)$",str):
            # todo ordinal unfolding
            if str.endswith(u"я"): self.numword.inflection_case = u"им,жр"
            elif str.endswith(u"х"): self.numword.inflection_case = u"рд,мн"
            elif str.endswith(u"е"): self.numword.inflection_case = u"ср,им" # -е: ср,им / мн,им
            elif str.endswith(u"ми"): self.numword.inflection_case = u"тв,мн"
            elif str.endswith(u"му"): self.numword.inflection_case = u"рд,ед,мр"
            elif str.endswith(u"го"): self.numword.inflection_case = u"рд,ед,мр"
            else: self.numword.inflection_case = u"им" #if str.endswith(u""): self.numword.inflection_case = u"им"
            # -й: мр,им / жр,тв красивый/красивой
            # -м: мр,тв / мр,пр красивым/красивом
            # -ю: восьмую / восьмою todo что делать?
            return self.numword.ordinal(self.get_canonical_number_from_string(re.sub('\D','',str)))
        else: return False

    def percentage(self,number,power=0):
        percent = [u"процент",u"промилле",u"промириад"]
        if long(number)!=number: return self.numword.cardinal(number)+ u" процента"
        else: return self.numword._split(number, hightxt=percent[power],split_precision=0)

    def short_endings(self,str):
        return str

    def complex_endings(self,str,number):
        self.numword.inflection_case = u"рд"
        return unicode(re.sub(" ","",self.numword.cardinal(number).upper()).lower())+re.sub("[\d-]","",str)

    def temperature(self,number):
        return self.numword._split(number,self.degree,split_precision=0)

    def detect_inflection(self,details):
        prep = ""
        gr_num = set()
        gr_case = set()
        gr_gend = set()
        # most popular russian prepositions and corresponding cases
        preps = { # todo make better resolving for prepositions with multiple cases
            u"им":set(),
            u"рд":{u'от', u'до', u'из', u'изо', u'без', u'безо', u'у', u'для', u'около', u'с', u'со', u'вокруг', u'после', u'кроме'},
            u"дт":{u'к', u'ко', u'по'},
            u"вн":{u'во', u'на', u'за', u'про', u'через', u'по'}, # u'в'
            u"тв":{u'с', u'со', u'за', u'под', u'подо', u'над', u'надо', u'между', u'перед', u'пред'},
            u"пр":{u'о', u'об', u'обо', u'в', u'во', u'на', u'при'},
        }
        # if it's a date then it should be ordinal, not cardinal number — @type is 'ord'/'card'
        ordinal_case = set(self.all_forms(u'число')) | set(self.all_forms(u'год')) | {u'г.',u'Г.',u'гг.',u'ГГ.'}
        for month in self.months:
            ordinal_case|=set(self.all_forms(month))
        if len(details['right']) > 0 and re.sub(u'Ё',u'Е',details['right'][0].upper()) in ordinal_case or len(details['left']) > 0 and re.sub(u'Ё',u'Е',details['left'][-1].upper()) in ordinal_case:
            type = "ord"
            if details['right'][0] in {u'г.',u'Г.',u'гг.',u'ГГ.'}: gr_gend = {u'мр'}
            else:  gr_gend = {u'ср'}
        else: type = "card"

        # checking with words after the number
        grammeme_r = []; grammeme_l = []
        for word in details['right']:
            grammeme_r = [set()] # todo support multiple predecessing words
            gram_info = self.numword.morph.get_graminfo(word.upper())
            for graminfo_hypo in gram_info:
                #print "    ####__right",word,repr(graminfo_hypo).decode("unicode-escape")
                if graminfo_hypo['class'] == u"С" or graminfo_hypo['class'] == u"ПРИЛ":
                    grammeme_r[0] |= set(graminfo_hypo['info'].split(','))

        # checking with words before the number and prepositions
        for word in details['left']:
            grammeme_l = [set()]
            gram_info = self.numword.morph.get_graminfo(word.upper())
            for graminfo_hypo in gram_info:
                #print "    ####__left",word,repr(graminfo_hypo).decode("unicode-escape")
                if graminfo_hypo['class'] == u"ПРЕДЛ":
                    # preposition just before the number
                    for c in preps:
                        if word.lower() in preps[c]:
                            gr_case.add(c)
                elif graminfo_hypo['class'] == u"С" or graminfo_hypo['class'] == u"ПРИЛ":
                    grammeme_l[-1] |= set(graminfo_hypo['info'].split(','))
        if gr_case: # there is a proposition before the number
            if len(details['right']) > 0 and len(gr_case & grammeme_r[0] & self.cases) > 0: # intersection of 2 hypotheses of prep before and noun after the number
                return gr_case & grammeme_r[0] & self.cases,self.numrs & grammeme_r[0],self.genders & grammeme_r[0],type
            else: gr_num = {u'ед'}
        elif grammeme_r[0]: # else we look only at the word after
            gr_case = self.cases & grammeme_r[0]
            gr_num = self.numrs & grammeme_r[0]
            gr_gend = self.genders & grammeme_r[0]
        elif grammeme_l[-1]: # otherwise only at the word before
            gr_case = self.cases & grammeme_l[-1]
            gr_num = self.numrs & grammeme_l[-1]
            gr_gend = self.genders & grammeme_l[-1]
        return gr_case,gr_num,gr_gend,type

    def all_forms(self,word,one_form = False):
        all = []
        if not isinstance(word,list): word = [word]
        for w in word:
            for numb in self.numrs:
                for case in self.cases:
                    all.append(self.numword.morph.inflect_ru(w.upper(), case + u',' + numb))
        return all

