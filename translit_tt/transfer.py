import glob
import os
import sys
import yaml
import logging
from cy2lt import tatar_trans
sys.path.append('../')

class transfer():
    def __init__(self):
        yml_files=glob.glob('./alphabet/*.yml')
        assert len(yml_files)!=0,'Any yaml file is not exist'

        self.alphabets_list=dict()
        for file in yml_files:
            assert os.path.exists(file),'{} is not exist'.format(file)
            try:
                with open(file, 'r') as f:
                    yml = yaml.safe_load(f)
                    self.alphabets_list[file.rsplit('/',1)[-1].rsplit('.',1)[0]] = yml
                    
            except Exception as e:
                print('Exception occurred while loading YAML...',file=sys.stderr)
                print(e, file=sys.stderr)
                sys.exit(1)

        self.alphabets_list['tat'] = 'this is unknown'
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
