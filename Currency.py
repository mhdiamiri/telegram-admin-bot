import requests

def all_coins():
    coins = ['BTC/USDT', 'ETH/USDT', 'LTC/USDT']
    ress = []
    for coin in coins:
        ress.append(requests.get('https://api.livecoin.net/exchange/ticker?currencyPair=%s'%coin))
    
    text = ''
    for i in ress:
        c = i.json()
        text += c['symbol']+ ':\n'
        text += 'Price: ' + str(int(c['last']*100) / 100 ) + '\n\n'

    return text
