from pathlib import Path
from bs4 import BeautifulSoup
import os
import json
import re
import ast
import math

#Alvin Yee: 38683118, yeeao, yeeao@uci.edu
#Travis Chong: 16101685, tchong2, tchong2@uci.edu


def run():
    DEV_path = r"C:"
    URL_path = r"C:"
    Index1_path= r"C:"
    Index2_path = r"C:"
    Index3_path = r"C:"
    Index4_path = r"C:"
    Index5_path = r"C:"
    Index6_path = r"C:"
    
    folders = [x[0] for x in os.walk(DEV_path)]
    #print('start')
    d = DEV_path
    index_map1 = {} #dictionary holds {url: score} #a-e, 0
    index_map2 = {} #dictionary holds {url: score} #f-i, 1-2
    index_map3 = {} #dictionary holds {url: score} #j-m, 3
    index_map4 = {} #dictionary holds {url: score} #n-q, 4-5
    index_map5 = {} #dictionary holds {url: score} #r-u, 6-7
    index_map6 = {} #dictionary holds {url: score} #v-z, 8-9
    
    url_dict = {} #dict for mapping int keys to url values: {int: url}
    url_dict_counter = 1 #counter for url_dict
    
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        print(full_path)
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            with open(Path(file_path)) as text:
                
                line = text.readline().strip()
                dict_json = json.loads(line) #use json to convert json string into a dict
                current_url = dict_json['url']
                if not current_url in url_dict.values():
                    url_dict[url_dict_counter] = current_url #map int to url
                    url_dict_counter += 1 #increment url counter
                    
                content = BeautifulSoup(dict_json['content'],features='lxml')
                html_text = content
                #print(html_text)
                tags_list = [str(tag.string) for tag in html_text.find_all([f'h{i}' for i in range(1,7)])]
                title_list = [str(tag.string) for tag in html_text.find_all(f'title')] #this is all the title and header text
                tags_list += [str(tag.string) for tag in html_text.find_all(f'strong')]#this is for getting bolded text
                tags_list += [str(tag.string) for tag in html_text.find_all(f'b')]#this is for getting bolded text
                tags_list += title_list #weigh the titles twice as much

                content = content.get_text().rstrip().split(' ') #Get content tag element
                for i in range(5): #add weight to title header and bolded text
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
                    if token[0] in "abcde0":
                        if token not in index_map1:
                            index_map1[token] = {}
                        index_map1[token][url_dict_counter-1] = sub_dict[token] #In index_map1, {word: {url_int:key}}
                    if token[0] in "fghi12":
                        if token not in index_map2:
                            index_map2[token] = {}
                        index_map2[token][url_dict_counter-1] = sub_dict[token] #In index_map2, {word: {url_int:key}}
                    if token[0] in "jklm3":
                        if token not in index_map3:
                            index_map3[token] = {}
                        index_map3[token][url_dict_counter-1] = sub_dict[token] #In index_map3, {word: {url_int:key}}
                    if token[0] in "nopq45":
                        if token not in index_map4:
                            index_map4[token] = {}
                        index_map4[token][url_dict_counter-1] = sub_dict[token] #In index_map3, {word: {url_int:key}}
                    if token[0] in "rstu67":
                        if token not in index_map5:
                            index_map5[token] = {}
                        index_map5[token][url_dict_counter-1] = sub_dict[token] #In index_map4, {word: {url_int:key}}
                    if token[0] in "vwxyz89":
                        if token not in index_map6:
                            index_map6[token] = {}
                        index_map6[token][url_dict_counter-1] = sub_dict[token] #In index_map4, {word: {url_int:key}}
                                
                
                if url_dict_counter == 18500 or url_dict_counter == 37000: #offload to disk after 1/3 and 2/3
                    #merge_dict = {} #create dict to merge existing index into
                    print("merge")
                    oldIndex = Translate(Index1_path)
                    newIndex = Merge(oldIndex, index_map1)
                    toFile(Index1_path, newIndex) #Merge index1
                    oldIndex = Translate(Index2_path)
                    newIndex = Merge(oldIndex, index_map2)
                    toFile(Index2_path, newIndex) #Merge index2
                    oldIndex = Translate(Index3_path)
                    newIndex = Merge(oldIndex, index_map3)
                    toFile(Index3_path, newIndex) #Merge index3
                    oldIndex = Translate(Index4_path)
                    newIndex = Merge(oldIndex, index_map4)
                    toFile(Index5_path, newIndex) #Merge index4
                    oldIndex = Translate(Index5_path)
                    newIndex = Merge(oldIndex, index_map5)
                    toFile(Index6_path, newIndex) #Merge index5
                    oldIndex = Translate(Index6_path)
                    newIndex = Merge(oldIndex, index_map6)
                    toFile(Index6_path, newIndex) #Merge index6
            
       #for loop end
       

    #print("num docs: ", url_dict_counter - 1)
    print("merge")
    oldIndex = Translate(Index1_path)
    newIndex = Merge(oldIndex, index_map1)
    toFile(Index1_path, newIndex) #Merge index1
    

    oldIndex = Translate(Index2_path)
    newIndex = Merge(oldIndex, index_map2)
    toFile(Index2_path, newIndex) #Merge index2
    
    oldIndex = Translate(Index3_path)
    newIndex = Merge(oldIndex, index_map3)
    toFile(Index3_path, newIndex) #Merge index3


    with open(Path(URL_path),'w') as urls:
        for key in url_dict.keys():
            urls.write(str(key) + "  ")
            urls.write(str(url_dict[key]))
            urls.write('\n')

    Calculate(Index1_path, url_dict_counter - 1) #calculate tf-idf
    Calculate(Index2_path, url_dict_counter - 1)
    Calculate(Index3_path, url_dict_counter - 1)
    Calculate(Index4_path, url_dict_counter - 1)
    return

def Translate(index_path): #translate index files back to dictionaries
    index_dict = {}
    filepath = Path(index_path)
    with open(str(filepath), "r") as index:
        for line in index:
            lineList = line.split("  ")
            subDict = ast.literal_eval(lineList[1].strip())
            
            index_dict[lineList[0]] = subDict
            
    return index_dict
    
def Merge(oldDict, currDict): #merge 2 index dictionaries
    mergedDict = oldDict

    for token in currDict.keys():
        if not token in mergedDict.keys():
            mergedDict[token] = currDict[token] #add new token entries
        else:
            for subDict in currDict[token]:
                #if not subDict in mergedDict[token]:
                mergedDict[token][subDict] = currDict[token][subDict] #add new url entries
    
    return mergedDict

def Calculate(index_path, totalLength): #calculate tf-idf score and replace in index
    indexDict = Translate(index_path)

    for token in indexDict.keys():
        df = len(indexDict[token])
        for url in indexDict[token]:
            tf = 1 + math.log10(indexDict[token][url])
            idf = totalLength/df
            idf = math.log10(idf)
            wtd = tf*idf
            indexDict[token][url] = wtd
    with open(Path(index_path),'w') as index: #Replace index
        for key in indexDict.keys():
            index.write(str(key) + "  ")
            index.write(str(indexDict[key]))
            index.write('\n')

def toFile(index_path, indexDict): #write index to file
    with open(Path(index_path),'w') as index: #Replace index
        for key in indexDict.keys():
            index.write(str(key) + "  ")
            index.write(str(indexDict[key]))
            index.write('\n')

    
if __name__ == '__main__':
    run()

