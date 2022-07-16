import json
import requests

import random
from my_list import *

def rchao():
    return random.choice(dchao)

def rkeu():
    return random.choice(dkeu)

def rbuon():
    return random.choice(dongvien)

def rchui():
    return random.choice(dchui)

def rkho():
    return random.choice(dkho)

def cero():
    return random.choice(erros)

# Hàm check số
def cint(message):
    try:
        int(message)
        return True
    except ValueError:
        return False


# <editor-fold desc="API">
# Hàm lấy quote
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = "\"" + json_data[0]['q'] + "\" - " + json_data[0]['a'] + " - "
    return (quote)

# Hàm love calculater
def love_calculater(f, m):
    url = "https://love-calculator.p.rapidapi.com/getPercentage"

    querystring = {f"sname": {m}, "fname": {f}}

    headers = {
        'x-rapidapi-host': "love-calculator.p.rapidapi.com",
        'x-rapidapi-key': "572afded3dmshb0a91ea8ac1ebf7p195510jsn8f9b44d954e1"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)

    out = '{}   ❤️  {} = {}% - {}'.format(data['fname'], data['sname'], data['percentage'], data['result'])

    return(out)

# Hàm joke
def hiujokes():

    url = "https://dad-jokes.p.rapidapi.com/random/joke/"

    headers = {
        'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
        'x-rapidapi-key': "572afded3dmshb0a91ea8ac1ebf7p195510jsn8f9b44d954e1"
    }

    response = requests.request("GET", url, headers=headers)

    data = json.loads(response.text)
    try:
        out = '{}\n- {}'.format(data['body'][0]['setup'], data['body'][0]['punchline'])
    except:
        out = 'Quá lượt joke hôm nay r 😢 muốn thêm thì donate đi'

    return (out)


# </editor-fold>