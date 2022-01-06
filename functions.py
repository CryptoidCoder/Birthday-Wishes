import requests, json
from dotenv import load_dotenv
import os

load_dotenv()


# Notion:
token = os.getenv('notion_token')
databaseId = os.getenv('Birthday-databaseId')


def readDatabase(databaseId): #read a databse and save to file
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2021-08-16"
    }

    res = requests.request("POST", readUrl, headers=headers)
    data= res.json()
    #print(f"Read Database : {res.status_code}")
    #print(res.text)
    
    with open('./db_read.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

def createrow(newPageData): #create a page in notion

    createUrl = 'https://api.notion.com/v1/pages'
    
    headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
    }

    data = json.dumps(newPageData)
    #print(newPageData)

    res = requests.request("POST", createUrl, headers=headers, data=data)

    #print(res.status_code)
    #print(f"Create Row : {res.status_code}")

def archiverow(rowId): #update a page with the archived=True tag in notion
    updateUrl = f"https://api.notion.com/v1/pages/{rowId}"

    headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
    }

    deletionData = {
        "archived": True
    }

    data = json.dumps(deletionData)

    res = requests.request("PATCH", updateUrl, headers=headers, data=data)

    #print(res.status_code)
    #print(f"Archived Row ({rowId}): {res.status_code}")

def updaterow(rowId, updateData): #update a page in notion
    rowId = rowId.replace("-", "") #remove all -
    updateUrl = f"https://api.notion.com/v1/pages/{rowId}"

    headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
    }

    data = json.dumps(updateData)

    res = requests.request("PATCH", updateUrl, headers=headers, data=data)
    return res.status_code

def extract_element_from_json(obj, path): #extract element from data
    '''
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    '''
    def extract(obj, path, ind, arr):
        '''
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        '''
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr

def getdata(dataset, path): #get data from json dataset
    parsed_data = extract_element_from_json(dataset, path)
    #print(f"parsed_data ({path}) : {parsed_data}")
    string_data = ""
    for item in parsed_data:
        try:
            string_data = string_data + item
            return str(string_data)
        except:
            return None
