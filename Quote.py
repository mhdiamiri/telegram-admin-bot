import requests

def get_Quote():
    response = requests.get('https://api.codebazan.ir/dialog/')
    return response.text