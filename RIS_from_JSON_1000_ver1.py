import json 
import re
import chardet
from os import listdir
from os.path import isfile, join


path_files = "/home/Desktop/json-gsheet/"

list_of_files = ['/home/Desktop/json-gsheet/'+f for f in listdir(path_files) 
                 if isfile( join(path_files, f)) and f[-5:]=='.json']



def detect_file_encodind (file_name):
    with open(file_name, "rb") as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
    return result['encoding']

def write_json_file(file_name, enc, json_obj):
    with open(file_name, 'w',encoding=enc) as f:
        f.write(json.dumps(json_obj))

def clean_json_file (file_name, enc):
    with open(file_name, 'r', encoding=enc) as f:
        s = f.read()
        s = re.sub(r'NaN',"\"\"",s)
        s = re.sub(r'\\n','',s)
    obj = json.loads(s)
    return obj

def create_ris_format(json_object):
    json_to_ris = {"ArticleTitle":"TI", "Author(s)":"AU", "Source":"T2", 
                   "Date":"DA", "Page":"SP", "Page":"EP", "Persistent URL":"UR",
                   "PlaceofPublication":"CY" }
    ris_str = ''
   
    for key, value in json_object.items():
        data = json_object[key]
        ris_atr = json_to_ris.get(key)
        if not data:
            continue
        if not ris_atr:
            continue
            
        ris_str = ris_str + ris_atr + ' - ' + str(data) + '\n'
    ris_str = ris_str + 'ER-\n\n'
    return ris_str

i = 0 
ris = ''
"""for f in list_of_files:
    try:
        json_obj = clean_json_file(f,detect_file_encodind(f))
        print(type(json_obj))
        ris = ris + create_ris_format(json_obj)
    except Exception as ex:
        print(ex)
       
        
with open('/home/ostap/Desktop/json_to_ris' + '.ris','w') as r:
    r.write(ris)
"""
                
i = 1 
j = 1 
ris = ''
for f in list_of_files:
    try:
        json_obj = clean_json_file(f,detect_file_encodind(f))
        ris = ris + create_ris_format(json_obj)
        i = i + 1
        print(i)
        if i == 1000:
            print("if block ", j )
            with open('/home/ostap/Desktop/json_to_ris'+ str(j) + '.ris','w') as r:
                r.write(ris)
                i = 1
                j = j + 1
                ris = ''
    except Exception as ex:
         print(ex)
    
with open('/home/Desktop/json_to_ris'+ str(j) + '.ris','w') as f:
     f.write(ris)
