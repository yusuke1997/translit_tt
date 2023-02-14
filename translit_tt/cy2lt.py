import string

class tatar_trans():

    def __init__(self):
        self.capital = {"А", "Ә", "Б", "В", "Г", "Д", "Е", "Ё",
                        "Ж", "Җ", "З", "И", "Й", "К", "Л", "М",
                        "Н", "Ң", "О", "Ө", "П", "Р", "С", "Т",
                        "У", "Ү", "Ф", "Х", "Һ", "Ц", "Ч", "Ш",
                        "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"}
        
        self.back = {"а", "ы", "о", "у", "ъ", "a", "ı", "o", "u",
                     "ya", "yu", "yı",
                     "А", "Ы", "О", "У", "Ъ", "A", "I", "O", "U",
                     "Ya", "Yu", "Yı",  ""}
        
        self.front = {"i", "ü", "ö", "ä", "e",
                      "и", "ү", "ө", "ә", "ь","е",
                      "İ", "Ü", "Ö", "Ä", "E",
                      "И", "Ү", "Ө", "Ә", "Ь","Е"}

        self.simple_rules = {"а":"a","б":"b","в":"w",
                             "д":"d","ж":"j","җ":"c","з":"z",
                             "и":"i","й":"y","л":"l","м":"m",
                             "н":"n","ң":"ñ","о":"o","ө":"ö",
                             "п":"p","р":"r","с":"s","т":"t",
                             "ф":"f","х":"x","һ":"h","ц":"ts",
                             "ч":"ç","ш":"ş","щ":"şç","ы":"ı",
                             "А":"A","Ә":"Ä","Б":"B","В":"W",
                             "Д":"D","Ж":"J",
                             "Җ":"C","З":"Z","И":"İ","Й":"Y",
                             "Л":"L","М":"M","Н":"N","Ң":"Ñ",
                             "О":"O","Ө":"Ö","П":"P","Р":"R","С":"S",
                             "Т":"T","У":"U","Ү":"Ü","Ф":"F",
                             "Х":"X","Һ":"H","Ц":"Ts","Ч":"Ç",
                             "Ш":"Ş","Ы":"I","Ь":"",
                             "Э":"E","Ю":"Yu"
                             }

        self.special_vowel_rules = {"а":"ä","о":"ö","у":"ü","ы":"e"}
        
    def simple_rulebase(self,char):
        assert char in self.simple_rules, '{} is not in simple_rules'.format(char)
        return self.simple_rules[char]

    def split_vowel(self,word):
        split_list=list()
        i=0
        while(i != len(word)):
            #print(word)
            if word[i] in self.back or word[i] in self.front or word[i] in string.punctuation:
                subword,word=word[:i+1],word[i+1:]
                split_list.append(subword)
                i=0
            else:
                i+=1

        if len(word) != 0:
            split_list.append(word)            
        return split_list

    def next_vowel(self,word,index):
        split_word = self.split_vowel(word)
        split_word_index = [len(elm) for elm in split_word]
        count = -1
        #print(word[index])
        for i in range(len(split_word)):
            count+= len(split_word[i])
            if count>=index:
                break
        #print(i,len(split_word))
        if i == len(split_word)-1:
            return (False,None)
        i+=1#next word

        #return is tuple type
        #So, (Boolean,content)
        #if it is false, (False,None) else (True, value)
        
        return (True,split_word[i][-1])

    def current_vowel(self,word,index):
        split_word = self.split_vowel(word)
        split_word_index = [len(elm) for elm in split_word]
        count = -1
        #print(word[index])
        for i in range(len(split_word)):
            count+= len(split_word[i])
            if count>=index:
                break
        return (True,split_word[i][-1])

    def prev_vowel(self,word,index):
        split_word = self.split_vowel(word)
        split_word_index = [len(elm) for elm in split_word]
        count = -1
        #print(word[index])
        for i in range(len(split_word)):
            count+= len(split_word[i])
            try:
                if count>=index:
                    break
            except:
                continue
        if i==0:
            return (False,None,None)
        #print(split_word)
        i-=1
        return (True,split_word[i][-1],sum(split_word_index[:i+1])-1)
        

    def prev_letter(self,word,i):
        return word[i-1] if i != 0 else None

    def next_letter(self,word,i):
        return word[i+1] if i != len(word) -1 else None

    def special_vowel(self,word,index):
        #ここ疑問手
        #もうちょっといい書き方あるんじゃないかなあ
        #current_vowel = self.current_vowel(word,index)
        current_vowel = (True,word[index])
        next_vowel = self.next_vowel(word,index)
        
        if current_vowel[0] and current_vowel[1] in self.special_vowel_rules \
           and next_vowel[0] and next_vowel[1] in self.front:
            return (True,self.special_vowel_rules[word[index]])
    
        return (False,None)

    def last_latin_word(self,words,i):
        return words[i-1] if len(words) != 0 else None
    
    #def complex_rules(self,andmoreargument...):    

    def trans(self,sentence):
        cyrillic = list(sentence.split()) #list for each word
        for j in range(len(cyrillic)):
            letters = list(cyrillic[j]) #list for each letter
            latinwords = ['']*len(letters)
            i = 0
            #for i in range(len(letters)): #convert each letter
            while(i<len(letters)):
                #print(letters)
                #記述がめんどいからちょっと計算重くなるけどこうやって書き換える
                prev_vowel = self.prev_vowel(letters,i)[1]
                next_vowel = self.next_vowel(letters,i)[1]
                current_vowel = self.current_vowel(letters,i)[1]
                next_letter = self.next_letter(letters,i)
                prev_letter = self.prev_letter(letters,i)
                last_word = self.last_latin_word(latinwords,i)
                
                if letters[i] in self.simple_rules:
                    latinwords[i] = self.simple_rulebase(letters[i])

                elif letters[i] == "ә":
                     _,prev_vowel,index1 = self.prev_vowel(letters,i)
                     if prev_vowel == "ы" and letters[index1+1] == "й":#ここ要修正
                         latinwords[index1] = "i"
                         latinwords[index1+1] = ""
                         latinwords[i] = "ä"
                     else:
                         latinwords[i] = "ä"
                
                elif letters[i] == "г":
                    if i == len(letters)-1:
                        latinwords[i] = "g"
                    elif current_vowel in self.back or prev_vowel in self.back:
                        latinwords[i] = "g" if current_vowel in self.front else "ğ" 
                        #ここもうちょっと良い書き方ある気がする
                        special_letter = self.special_vowel(letters,i+1)
                        if special_letter[0]:
                            latinwords[i+1] = special_letter[1]
                            if letters[i+1] == "у" and self.next_letter(letters,i+1) in (self.front - {'е'}):
                                latinwords[i+1]+='w'
                            i+=1
                    else:
                        latinwords[i] = "g"

                elif letters[i] == "Г": #大文字版
                    if i == len(letters)-1:
                        latinwords[i] = "G"
                    elif current_vowel in self.back or prev_vowel in self.back:
                        latinwords[i] = "G" if (current_vowel in self.front) else "Ğ"
                        special_letter = self.special_vowel(letters, i+1)
                        if special_letter[0]:
                            latinwords[i+1] = special_letter[1]
                            if letters[i+1] == "у" and self.next_letter(letters, i+1) in self.front:
                                latinwords[i+1] += "w"
                            i += 1
                        
                elif letters[i] == "е":
                    if i != 0:
                        if (prev_letter in self.back or prev_letter == "-"): # and prev_letter not in ['у', 'У']:
                            latinwords[i] = "yı"
                        elif prev_letter in self.front and prev_letter not in ['ү', 'Ү']:
                            latinwords[i] = "ye"
                        else:
                            latinwords[i] = "e"
                    elif i == 0:
                            latinwords[i] = "ye" if (next_vowel in self.front and i == 0) else "yı"
                    else:
                        latinwords[i] = "e"

                elif letters[i] == "Е": #大文字版
                    if i != 0:
                        if prev_letter in self.back or prev_letter == "-":
                            latinwords[i] = "YI"
                        elif prev_letter in self.front:
                            latinwords[i] = "YE"
                        else:
                            latinwords[i] = "E"
                    elif i == 0:
                        latinwords[i] = "Ye" if (next_vowel in self.front and i == 0) else "Yı"
                    else:
                        latinwords[i] = "E"
                        
                elif letters[i] == "к":
                    if i == len(letters)-1:
                        latinwords[i] = "q" if (prev_vowel in self.back or prev_letter in ["я", "ю"] or last_word =="yı" ) else "k"
                    else:
                        if prev_vowel in self.back or current_vowel in self.back:
                            latinwords[i] = "k" if current_vowel in self.front else "q"
                            #ここの情報は次の単語だからちょっと書き方変えよう
                            special_letter = self.special_vowel(letters,i+1)
                            if special_letter[0]:
                                latinwords[i+1] = special_letter[1]
                                if letters[i+1] == "у" and self.next_letter(letters,i+1) in (self.front - {'е'}):
                                    latinwords[i+1]+='w'
                                i+=1
                        else:
                            latinwords[i] = "k"

                elif letters[i] == "у":
                    if i != 0 and prev_letter in ["а", "А", "я", "Я"]:
                        latinwords[i] = "w"
                    elif i != len(letters)-1:
                        if next_letter == "е": #e.g., буенча buyınça
                            latinwords[i] = "u" 
                        elif (next_letter in self.front or next_letter in self.back) and next_letter != "е":
                            latinwords[i] = "uw"
                        else:
                            latinwords[i] = "u"
                    else:
                        latinwords[i] = "u"
                        
                elif letters[i] == "ү":
                    if i != 0 and prev_letter in ["ә", "Ә", "я", "Я"]:
                        latinwords[i] = "w"
                    elif i != len(letters)-1:
                        latinwords[i] = "üw" if (next_letter == "е") else "ü"
                    else:
                        latinwords[i] = "ü"
                        
                elif letters[i] == "ь":#わけわかんね
                    _,prev_vowel,index1 = self.prev_vowel(letters,i)
                    _,prev_prev_vowel,index2 = self.prev_vowel(letters,index1)
                    #print(prev_vowel,prev_prev_vowel)
                    if i != len(letters)-1:
                        if next_letter == "я":
                            latinwords[i] = "ya"
                            latinwords[i+1] = ""
                            i+=1
                        elif next_letter == "е": #пьеса pyesa となるように
                            latinwords[i] = "ye"
                            latinwords[i+1] = ""
                            i+=1
                        elif next_letter == "ә":
                            latinwords[i] = "\'"
                        else:
                            latinwords[i] = ""
                    elif prev_vowel == "а":
                        latinwords[i] = ""
                        if prev_letter != prev_vowel:
                            temp = list(latinwords[i-2])
                            temp[-1] = "ä"
                            latinwords[i-2] = ''.join(temp)
                        else:
                            latinwords[i-1] = "ä"
                    elif prev_vowel == "у":
                        latinwords[i] = ""
                        if prev_letter != prev_vowel:
                            temp = list(latinwords[i-2])
                            temp[-1] = "ü"
                            latinwords[i-2] = ''.join(temp)
                        else:
                            latinwords[i-1] = "ü"

                    elif prev_vowel == "ю":
                        latinwords[i] = ""
                        if prev_letter != prev_vowel:
                            temp = list(latinwords[i-2])
                            temp[-1] = "yü"
                            latinwords[i-2] = ''.join(temp)
                        else:
                            latinwords[i-1] = "yü"
                            
                    elif prev_vowel == "ы" and letters[index1+1] == "й":#ここ要修正
                        latinwords[index1] = "i"
                        latinwords[index1+1] = ""
                        latinwords[i] = ""
                    else:
                        latinwords[i] = ""
                        
                elif letters[i] == "ъ":
                    latinwords[i] = "\'" if (next_letter in self.front | self.back) else ""

                elif letters[i] == "э":
                    latinwords[i] = "\'" if (i != 0 and prev_vowel in self.front | self.back) else "e"
                        
                elif letters[i] == "ю":
                    latinwords[i] = "yü" if ((next_vowel in self.front) or (i == len(letters)-1 and prev_vowel in self.front)) else "yu"
                    if next_letter in self.front | self.back and next_letter: # not in ['у', 'ү', 'У', 'Ү']:
                        latinwords[i] += 'w'
                    
                elif letters[i] == "я":
                    if i != 0:
                        latinwords[i] = "yä" if (prev_vowel in self.front) else "ya"
                    else:
                        latinwords[i] = "yä" if (current_vowel in self.front) else "ya"

                elif letters[i] == "Я": #大文字版
                    if i != 0:
                        latinwords[i] = "YÄ" if (prev_vowel in self.front) else "YA"
                    else:
                        if next_letter in self.capital:
                            latinwords[i] = "YÄ" if (current_vowel in self.front) else "YA"
                        else:
                            latinwords[i] = "Yä" if (current_vowel in self.front) else "Ya"
                        
                elif letters[i] == "К":
                    if i == len(letters)-1:
                        latinwords[i] = "Q" if (prev_vowel in self.back) else "K"
                    else:
                        if prev_vowel in self.back or current_vowel in self.back:
                            latinwords[i] = "K" if current_vowel in self.front else "Q"
                            #ここの情報は次の単語だからちょっと書き方変えよう                                                                                                                               
                            special_letter = self.special_vowel(letters,i+1)
                            if special_letter[0]:
                                latinwords[i+1] = special_letter[1]
                                if letters[i+1] == "у" and self.next_letter(letters,i+1) in self.front:
                                    latinwords[i+1]+='w'
                                i+=1
                        else:
                            latinwords[i] = "K"
                #elif letters[i] == "К":
                #    latinwords[i] = "Q" if (prev_vowel in self.back) else "K"

                else:
                    latinwords[i] = letters[i]

                if i != 0 and latinwords[i] in ['yı', 'ya', 'yu']:
                    candidate_vowel = {'ä':'a', 'ö':'o', 'ü':'u', 'e':'ı'}
                    latinwords[i-1] = candidate_vowel[latinwords[i-1]] if latinwords[i-1] in candidate_vowel else latinwords[i-1]
                     
                i+=1
                #print(latinwords)
            latinword = "".join(latinwords)
            cyrillic[j] = latinword
        latin = " ".join(cyrillic)
        return latin

if __name__ =='__main__':
    trans = tatar_trans()
    while(True):
        sentence = input()
        if sentence in ['\n','']:break
        result=trans.trans(sentence)
        print(result)

"""
i == len(letters)-1 を、Booleanをとる変数として定義できないか？
def last():
if i == len(letters)-1:
return True
"""

"""
語頭が大文字の時はどうする？
語頭が大文字の時の処理も作れば良い
"""

"""
гаепле ğäyeple
әдәбият ädäbiyat
мәдәният mädäniyat
буенча buyınça
вәзгыять wäzğiyät 正直、揺れがある
"""
"""
пьеса pyesa ok
Яшьләр Yäşlär ok
Елга Yılğa ok
Гомер Ğömer ok
юк yuq ok
ЮХИДИ YUXİDİ
кыен qıyın
кагыйдә qağidä ok
шагыйрь şağir ok
гаилә ğailä
каенның qayınnıñ
аятендә ayätendä
Лбищенскидан Lbişçenskidan ok
июль iyül
коелган qoyılğan
Якшәмбе Yäkşämbe
подъезда podyezda
куелды quyıldı
юуда yuwuda ok
Гадәттәгечә Ğädättägeçä ok
лаек layıq ok
як yaq ok
"""
