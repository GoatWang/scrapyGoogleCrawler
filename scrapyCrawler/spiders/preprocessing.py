import nltk
nltk.download('stopwords')
nltk.download('wordnet')
print('download nltk data success')

import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from os import listdir, stat

def preprocessing(companyStr):

    companyStr = companyStr.replace("\n"," ").replace("\t"," ").replace("\r"," ")

    i = 0
    while i < 30 :
        companyStr = companyStr.replace("  "," ")
        i+=1

    #re_words = re.compile(u"[\u4e00-\u9fa5]+")  ##drop chinese 
    re_words = re.compile(u"[\u3400-\u9FFF]+?") ##drop chinese korean japanese
    dropStrs = re.findall(re_words, companyStr)
    if len(dropStrs) != 0:
        for ds in dropStrs:
            companyStr = companyStr.replace(ds,"")

    re_words = re.compile('\{.*\}' )
    dropStrs = re.findall(re_words, companyStr)
    if len(dropStrs) != 0:
        for ds in dropStrs:
            companyStr = companyStr.replace(ds,"")

    re_words = re.compile('[\d]+')
    dropStrs = re.findall(re_words, companyStr)
    if len(dropStrs) != 0:
        for ds in dropStrs:
            companyStr = companyStr.replace(ds,"")

    for pun in string.punctuation+"©":
        companyStr = companyStr.replace(pun, "")

    stops = list(set(stopwords.words('english')))
    lemmer = WordNetLemmatizer()

    if __name__ == '__main__':
        file = open('statesFilter/stateSimilars', 'r',encoding='utf8')
    else:
        file = open('scrapyCrawler/spiders/statesFilter/stateSimilars', 'r',encoding='utf8')

    for line in file:
        stops.append(line.replace("\n",""))
    file.close()

    def isfilter(s):
        return any(not i.encode('utf-8').isalpha() for i in s)

    companyStr = companyStr.lower().strip()
    companyStr.replace('®','')

    paramStr = ""
    for i in companyStr.split():
        try:
            if ((i not in stops) and (not isfilter(i))):
                paramStr += lemmer.lemmatize(i)+ " "
        except:
            continue

    return paramStr

if __name__ == '__main__':
    testingStr = "brands the cocacola company the cocacola company the cocacola company locations africa morocco french asia pacific australia china hong kong india japan new zealand eurasia middle east arabic middle east english pakistan english pakistan urdu russia europe austria belgium dutch belgium french denmark finland france germany great britain ireland italy netherlands norway portugal poland spain sweden switzerland ukraine latin america argentina bolivia brazil chile colombia costa rica dominican republic ecuador el salvador guatemala honduras mexico nicaragua panama paraguay peru uruguay venezuela north america global canada english canada french locations investors  the cocacola company our company our company main about cocacola journey mission vision  values diversity  inclusion human and workplace rights workplace overview supplier diversity cocacola leaders the cocacola system company history company reports sustainability report cocacola product facts us the cocacola foundation world of cocacola cocacola store investors investors main  year in review investors info financial reports and information investors info stock information investors info investor webcasts and events shareowner information corporate governance investors info sec filings press center press center main press releases company statements leadership video library image library press contacts careers careers main contact us contact us main faqs by cokestyle  sustainability report water replenishment giving back diversity  inclusion our commitment to transparency brands the cocacola company cocacola sprite fanta diet coke cocacola zero cocacola life dasani minute maid ciel powerade simply orange cocacola light fresca glacéau vitaminwater del valle glacéau smartwater mello yello fuze fuze tea honest tea odwalla powerade zero cocacola freestyle world of cocacola cocacola store close the cocacola company view product description all social facebook instagram twitter google youtube linkedin visit facebook visit instagram visit twitter visit google visit youtube visit linkedin load more cocacola on social likes followers followers views followers"
    print(preprocessing(testingStr))        
    # preprocessing(testingStr)        


