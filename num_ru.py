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
            elif str.endswith(u"ми"): self.numword.inflection_case = u"тв,мн"
            elif str.endswith(u"му"): self.numword.inflection_case = u"рд,ед,мр"
            elif str.endswith(u"го"): self.numword.inflection_case = u"рд,ед,мр"
            else: self.numword.inflection_case = u"им" #if str.endswith(u""): self.numword.inflection_case = u"им"
            # -й: мр,им / жр,тв красивый/красивой
            # -м: мр,тв / мр,пр красивым/красивом
            # -е: ср,им / мн,им
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