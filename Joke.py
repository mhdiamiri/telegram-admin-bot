import requests

def tell_joke():
    response = requests.get('https://api.codebazan.ir/jok/')
    return response.text
