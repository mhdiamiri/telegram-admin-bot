import requests

def get_bio():
    response = requests.get('https://api.codebazan.ir/bio/')
    return response.text
