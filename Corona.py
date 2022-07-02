import requests

def corona_iran():
    response = requests.get('https://api.codebazan.ir/corona/?type=country&country=Iran')
    js = response.json()['result']
    text = 'Country: Iran\n\n'
    text += 'cases: ' + str(js['cases']) + '\n\n'
    text += 'deaths: '+ str(js["deaths"]) + '\n\n'
    text += 'recovered: ' + str(js['recovered'])
    return text
