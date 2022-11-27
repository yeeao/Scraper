from pathlib import Path
from bs4 import BeautifulSoup
import os
import json
import re

#Alvin Yee: 38683118, yeeao, yeeao@uci.edu
#Travis Chong: 16101685, tchong2, tchong2@uci.edu

#figure out idf score thing

#get header or other important info to add to tokens/frequency


def run():
    DEV_path = r"C:\Users\Travis\Desktop\DEV"
    folders = [x[0] for x in os.walk(DEV_path)]
    print('start')
    d = DEV_path
    index_map = {} #main dictionary holds key:word, with value: {url:score}
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        print(full_path)
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            with open(Path(file_path)) as text:
                
                line = text.readline().strip()
                dict_json = json.loads(line) #use json to convert json string into a dict
                current_url = dict_json['url']
                content = BeautifulSoup(dict_json['content'],features='lxml')
                html_text = content
                #print(html_text)
                tags_list = [str(tag.string) for tag in html_text.find_all([f'h{i}' for i in range(1,7)])]
                tags_list += [str(tag.string) for tag in html_text.find_all(f'title')] #this is all the title and header text
                
                content = content.get_text().rstrip().split(' ') #Get content tag element
                content+= tags_list
                
                
                #tokenizing from previous assignment
                tokens = []
                for word in content:
                    tWord = re.split('[^0-9A-Za-z]+',word) #splits the string into words by the nonalphanumeric counters
                    
                    for splitWords in tWord:
                        if splitWords != '' and splitWords and len(splitWords) > 1:
                            tokens.append(splitWords)
                sub_dict = {} #sub dictionary holding all tokens and frequency
                for token in tokens:
                    token = token.lower()
                    if token not in sub_dict:
                        sub_dict[token] = 0
                    sub_dict[token] += 1
                
                for token in sub_dict:
                    if token not in index_map:
                        index_map[token] = {}
                    index_map[token][current_url] = sub_dict[token] #In index_map, {word: {url:key}}
       # break
    doc_set = set()

    for key in index_map.keys():
        #print(key, index_map[key])
        doc_set.update(list(index_map[key].keys()))
    #print(doc_set)
    print("doc length: ", len(doc_set))

    with open(Path(r"C:\Users\Travis\Desktop\index.txt"),'w') as index:
         #index.write(str(index_map))
         for key in index_map.keys():
             index.write(str(key) + ": ")
             index.write(str(index_map[key]))
             index.write('\n')
            

                
    


if __name__ == '__main__':
    run()

