import glob
import os
import sys
import logging
from .cy2lt import tatar_trans

class trans:
    def __init__(self):

        self.alphabets_list= dict()
        self.alphabets_list['rus'] = {'Ё': 'Yo', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G','Д': 'D',
                                      'Е': 'E', 'Ж': 'J', 'З': 'Z', 'И': 'İ', 'Й': 'Y', 'К': 'K',
                                      'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
                                      'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'X', 'Ц': 'Ts',
                                      'Ч': 'Ç', 'Ш': 'Ş', 'Щ': 'Şç', 'Ъ': '', 'Ь': '', 'Ы': 'I',
                                      'Э': 'E', 'Ю': 'Yu','Я': 'Ya','а': 'a', 'б': 'b', 'в': 'v',
                                      'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'j', 'з': 'z', 'и': 'i',
                                      'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
                                      'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
                                      'х': 'x', 'ц': 'ts', 'ч': 'ç', 'ш': 'ş', 'щ': 'şç', 'ъ': '',
                                      'ы': 'ı', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ё': 'yo',
                                      'ия': 'iyä'}

        self.alphabets_list['tat'] = None
        self.tatar = tatar_trans()

    def tokenize(self,text,lang):
        new_text = list(text)
        i = 0
        while(i<len(new_text)-1):
            if new_text[i]+new_text[i+1] in self.alphabets_list[lang]:
                new_text[i] = new_text[i]+new_text[i+1]
                new_text.pop(i+1)
            i+=1
            
        return new_text
                
    def trans(self,src,lang):
        #print(src,lang)
        assert lang in self.alphabets_list,'{} is no define in alphabet lists'.format(lang)
        #print(src)
        if lang == 'tat':
            return self.tatar.trans(src)
        
        tgt=''
        src = self.tokenize(src,lang)
        for letter in src:
            if letter in self.alphabets_list[lang]:
                tgt+=self.alphabets_list[lang][letter]
            else:
                logging.warning('unwatched letter: {}'.format(letter))
                #print(src)
                #tgt+=letter
                tgt+=self.tatar.trans(letter)
        return tgt
        
if __name__ == '__main__':
    trans=trans()
    print(trans.alphabets_list)
