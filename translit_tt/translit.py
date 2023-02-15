from fasttext import load_model
import logging
import string
import codecs
import os
import sys
from subword_nmt import apply_bpe
from .transfer import trans
logger = logging.getLogger(__name__)

class translit():
    def __init__(self):
        self.trans = trans()
        self.FTLANG_CACHE = os.getenv("FTLANG_CACHE", "/tmp/translit_tt")
        self.model = self.get_or_load_model('model')
        self.codes = self.get_or_load_model('bpe')
        self.bpe = apply_bpe.BPE(codes=self.codes)
        self.table = str.maketrans('', '', string.punctuation)

    def download_model(self, name: str) -> str:
        FTLANG_CACHE = os.getenv("FTLANG_CACHE", "/tmp/translit_tt")
        _path = {'model': "https://www.dropbox.com/s/iist24l59kcrbv9/langdetect.bin",
                 'vocab': "https://www.dropbox.com/s/e06a3x6xbqua0jm/langdetect.vec",
                 'bpe'  : "https://www.dropbox.com/s/igiksyf2qkog9ts/model.bpe"}
        _name = {'model': 'langdetect.bin',
                 'vocab': 'langdetect.vec',
                 'bpe'  : 'model.bpe'}
        
        target_path = os.path.join(FTLANG_CACHE, _name[name])
        if not os.path.exists(target_path):
            logger.info(f"Downloading {name} model ...")

            os.makedirs(FTLANG_CACHE, exist_ok=True)
            with open(target_path, "wb") as fp:
                response = requests.get(_path[name])
                fp.write(response.content)
            logger.info(f"Downloaded.")
        return target_path

    def get_or_load_model(self, name: str):
        model_path = self.download_model(name)
        if name=='model':
            model = load_model(model_path)
        elif name=='bpe':
            model = codecs.open(model_path, encoding='utf-8')
        else:
            raise NotImplementedError
            
        return model

        
    def remove(self,sentence,lower_case=True,only_lower=False):
        words = sentence.split()
        stripped = [w.translate(self.table) for w in words]
        if lower_case:
            lower = [w.lower() for w in stripped]
        else:
            lower = stripped

        if only_lower:
            return ' '.join(lower)
        else:
            #よく考えたらここいらないじゃん
            return (' '.join(stripped),' '.join(lower))
            #return (' '.join(words),' '.join(lower))

    def predict_language(self,word, k=1):
        labels={'a','b'}
        subword_elements=[]
        subword=word.split()
        for elm in subword:
            label, prob = self.model.predict(elm, k)
            subword_elements.append((label,prob))
            if prob>0.8:
                labels.add(label)
                
        if len(labels)<2:
            return predict_language_word(word,model)
        else:
            return [(elm[0][0].replace("__label__", "").replace('@@ ',''),elm[1]) for elm in subword_elements]

    def predict_language_word(self,text, k=1):
        label, prob = model.predict(text, k)
        return list(zip([l.replace("__label__", "") for l in label], prob))

    
    def split_original_word_with_bpebase(self,word,bped_word):
        bped_word=[elm.replace('@@','') for elm in bped_word.split()]
        elm_length = list(map(len,bped_word))
        word = word.translate(self.table)
        if len(word) != sum(elm_length):
            return word
        new_word=''
        current_chr=0
        #ここ累積和使えばかっこいいね
        for length in elm_length:
            new_word+=word[current_chr:current_chr+length]+' '
            current_chr+=length

        #print(new_word)
        return new_word

    def concat_subword(self,head,predicted):
        new_head=['<BOS>']
        new_predicted=[(None,None)]
        head = head.split()
        i = 0
        while(i < len(predicted)):
            if new_predicted[-1][0] == predicted[i][0]:
                temp = new_predicted.pop()
                new_predicted.append((temp[0],max(*[temp[1] if temp[1] != None else 0.0],predicted[i][1])))
                temp = new_head.pop()
                new_head.append(temp+head[i])
            else:
                new_predicted.append(predicted[i])
                new_head.append(head[i])
            i+=1
        new_head = new_head[1:]
        new_predicted = new_predicted[1:]
        return ' '.join(new_head),new_predicted
            
    def fixed_subword(self,head,predicted):
        new_head=['<BOS>']
        new_predicted=[(None,None)]

        head = head+'  <EOS>'
        head = head.split()
        predicted = predicted + [(None,None)]
        i = 0
        while(i < len(predicted)-1):
            #print(head[i],predicted[i])
            #print(new_head)
            #これじゃ不完全
            if new_predicted[-1][0] == predicted[i+1][0] and new_predicted[-1][0] != predicted[i][0] \
               and new_predicted[-1][0] != None and predicted[i+1][0] != None and predicted[i][0] =='tat' \
               and not (predicted[i][1] > 0.99):
                temp = new_predicted.pop()
                new_predicted.append((temp[0],max(*[temp[1] if temp[1] != None else 0.0]\
                                                  ,predicted[i][1],\
                                                  *[predicted[i+1][1] if predicted[i+1][1] != None else 0.0])))
                temp = new_head.pop()
                new_head.append(temp+head[i]+head[i+1])
                i+=1
            else:
                new_predicted.append(predicted[i])
                new_head.append(head[i])
            i+=1
        new_head = new_head[1:]
        new_predicted = new_predicted[1:]
        return ' '.join(new_head),new_predicted

    def fixed_tat_rus_to_tat(self,head,predicted):#tat-rus のみの単語はtat認定する
        if len(predicted) ==2:
            if predicted[0][1]>0.99 and predicted[1][1]>0.99999:
                pass
            elif predicted[0][0] =='tat' and predicted[1][0]=='rus' and \
               (predicted[0][1]>=predicted[1][1] or predicted[0][1]>0.99 or (len(head.split()[0])==1 and len(head.split()[1])==1)):
                predicted = [('tat',max(predicted[0][1],predicted[1][1]))]
                head = ''.join(head.split())
            elif predicted[0][0] =='tat' and predicted[1][0]=='rus' and \
                 (predicted[1][1]>0.99 and predicted[0][1]<0.85):
                predicted = [('rus',max(predicted[0][1],predicted[1][1]))]
                head = ''.join(head.split())
            elif predicted[0][0] =='rus' and predicted[1][0]=='tat' and \
                 predicted[0][1]>0.99 and predicted[0][1]>=predicted[1][1]:
                predicted = [('rus',max(predicted[0][1],predicted[1][1]))]
                head = ''.join(head.split())
        return head,predicted

    def fix_only_one_word(self,head,predicted):#とりあえず一番最初と一番最後だけ
        temp = head.split()
        if len(temp[0][0])==1 and len(temp) > 1:
            temp[1]=temp[0]+temp[1]
            head = ' '.join(temp[1:])
            predicted.pop(0)
        else:
            head = ' '.join(temp)
        temp = head.split()
        if len(temp)==1 and len(temp) > 1:
            a = temp.pop()
            b = temp.pop()
            temp.append(a+b)
            predicted.pop()
        head = ' '.join(temp)
        return head,predicted

    
    def translit(self,words):
        deal_punctuation_words=''
        for s in words:
            if s in string.punctuation+'”':
                deal_punctuation_words+='  '+s+'  '
            else:
                deal_punctuation_words+=s
                
        transed_word=''
        for word in deal_punctuation_words.split(' '):
            if len(word) == 0:
                #あえて空白のところを入れているのでそのための対処方法として
                transed_word+=' '
                continue
            removed_word  = self.remove(word)
            #print(word,removed_word)
            if len(removed_word[0]) == 0:
                #すべてpunctationの場合
                transed_word+=word+' '
            elif len(removed_word[0]) ==len(word):
                #特にremoveするものがなかった場合
                subword = self.bpe.process_line(removed_word[1])
                head = self.split_original_word_with_bpebase(removed_word[0],subword)
                predicted=self.predict_language(subword)
                if predicted[0][0]=='tat' and predicted[-1][0]=='tat':
                    head=head.replace(' ','')
                    predicted=[('tat',predicted[0][1])]

                head,predicted = self.fixed_subword(head,predicted)
                head,predicted = self.concat_subword(head,predicted)
                head,predicted = self.fixed_tat_rus_to_tat(head,predicted)
                head,predicted = self.fixed_subword(head,predicted)
                head,predicted = self.concat_subword(head,predicted)
                
                for elm,lang in zip(head.split(),predicted):#最初のうちはとりあえず小文字でやってみよう
                    #print(elm,lang)
                    transed_word+=self.trans.trans(elm,lang[0])
                transed_word+=' '
                #print()
            else:
                assert False,'predict word is bitly strange: {}'.format(word)
        transed_word=transed_word.replace('  ','')
        if transed_word[-1]==' ':
            transed_word=transed_word[:-1]
        return transed_word
        
if __name__ =='__main__':
    pred = predict()
    while(True):
        words=input()
        if words in ['\n','']:break
        result=pred.translit(words)
        print(result)
        #print(predict_language(words,model)[0])
