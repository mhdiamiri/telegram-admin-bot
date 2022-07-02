import requests
import json

def search_city(name):
    text = ''
    response = requests.get('https://api.codebazan.ir/weather/?city=%s'%(name))
    ok = response.json()["result"]['استان'] != 'null'
    if ok:
        keys = ["result", "فردا", "شنبه", "یک شنبه", "دوشنبه", "سه شنبه", "چهار شنبه", "پنج شنبه", "آدینه"]
        for key in keys:
            try:
                res = response.json()[key]
                if key != 'result' : text += (key+':'+'\n')
            except:
                break
            for title in res:
                text += str(title)+": "+str(res[title])+"\n"
            text += '\n'
        return text
    else:
        return 'Not Found'
