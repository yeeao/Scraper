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
    
    Index_Path1 = r"C:\Users\Travis\Desktop\CS 121\Assignment 3-M3\index-1.txt"
    Index_Path2 = r"C:\Users\Travis\Desktop\CS 121\Assignment 3-M3\index-2.txt"
    Index_Path3 = r"C:\Users\Travis\Desktop\CS 121\Assignment 3-M3\index-3.txt"
    Index_Path4 = r"C:\Users\Travis\Desktop\CS 121\Assignment 3-M3\index-4.txt"
    Index_Path5 = r"C:\Users\Travis\Desktop\CS 121\Assignment 3-M3\index-5.txt"
    Index_Path6 = r"C:/Users/Travis/Desktop/CS 121/Assignment 3-M3/index-6.txt"
    URL_path = r"C:/Users/Travis/Desktop/CS 121/Assignment 3-M3/urls.txt"

    while True:
        query = input("Please enter your query(\'Q' to quit): ")
        if query == 'Q':
            return
        
        query = query.lower()
        search_dict = {}
        queryList = re.split('[^0-9A-Za-z]+',query)
        #queryList = sorted(queryList)
        subDictList = []
        totalURLS = set()
                
        for word in queryList:
            if word == "and" or word == '': #ignore 
                continue
            elif word[0] in "abcde0":
                filepath = Path(Index_Path1)
            elif word[0] in "fghi12":
                filepath = Path(Index_Path2)    
            elif word[0] in "jklm3":
                filepath = Path(Index_Path3)
            elif word[0] in "nopq45":
                filepath = Path(Index_Path4)
            elif word[0] in "rstu67":
                filepath = Path(Index_Path5)
            elif word[0] in "vwxyz89":
                filepath = Path(Index_Path6)

            with open(str(filepath), "r") as index:
                for line in index:
                    lineList = line.split("  ")
                    if lineList[0] == word:
                        subDict = ast.literal_eval(lineList[1].strip())
                        subDictList.append(subDict)
                        for i in subDict.keys():
                            totalURLS.add(i)
                        break
                    
        print("Results:")
        removeSet = set()
        for url in totalURLS:
            for subDict in subDictList:
                if url not in subDict.keys():
                    removeSet.add(url)
                    break
                
        totalURLS -= removeSet
        for url in totalURLS:
            if url not in search_dict:
                search_dict[url] = subDict[url]
            for subDict in subDictList:
                search_dict[url] += subDict[url]
                
        search_dict = dict(sorted(search_dict.items(), key=operator.itemgetter(1),reverse=True))
        
        with open(str(URL_path), "r") as urls: #get dict of url-int mapping
            urlList = urls.readlines()
            #urlDict = ast.literal_eval(temp[0])
            
        count = 0
        if len(search_dict.items()) == 0:
            print("No results found")
            continue
        for item in search_dict.items():
            url = urlList[item[0]-1].split("  ")[1].strip()
            print(url)
            count += 1
            if count == 5:
                break
        
    
if __name__ == '__main__':
    run()
