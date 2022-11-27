from pathlib import Path
from bs4 import BeautifulSoup
import os
import json
import re
import ast
import operator
#Alvin Yee: 38683118, yeeao, yeeao@uci.edu
#Travis Chong: 16101685, tchong2, tchong2@uci.edu


def run():
    Index_Path = r"C:\Users\Travis\Desktop\index.txt"
    filepath = Path(Index_Path)
    
    query = input()
    query = query.lower()
    search_dict = {}
    queryList = re.split('[^0-9A-Za-z]+',query)
    subDictList = []
    totalURLS = set()
    
    with open(str(filepath), "r") as index:
        for line in index:
            lineList = line.split("  ")
            #print(lineList[0])
            subDict = ast.literal_eval(lineList[1].strip())
            #print(subDict)
            if lineList[0] in queryList:
                subDictList.append(subDict)
                for i in subDict.keys():
                    totalURLS.add(i)
    #return
    print("Looped")
    removeSet = set()
    # Think of doing this by getting list of all key,value pairs in each subDict
    # Then check if key appears the same number of times as the len of the query
    for url in totalURLS:
        for subDict in subDictList:
            if url not in subDict.keys():
                removeSet.add(url)
                break
            
    totalURLS -= removeSet
    for url in totalURLS:
        if url not in search_dict:
            search_dict[url] = 0
        for subDict in subDictList:
            search_dict[url] += subDict[url]
            
    search_dict = dict(sorted(search_dict.items(), key=operator.itemgetter(1),reverse=True))
    print(search_dict)
    count = 0
    for item in search_dict.items():
        print(item)
        count += 1
        if count == 5:
            break
if __name__ == '__main__':
    run()
