from flask import Flask, render_template
from flask_socketio import SocketIO
from wit import Wit
from difflib import SequenceMatcher
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins='*')
# socketio = SocketIO(app)
client = Wit("2XWTIKVOL6RTJLGCQQ7OXDG6YQVBCTMH")

# dictionary for countries to api code
countries = {
    'Algeria': 'pp4Wo2slUJ78ZnaAi',
    'Austria': 'RJtyHLXtCepb4aYxB',
    'Azerbaijan': 'ThmCW2NVnrLa0tVp5',
    'Bahrain': 'c7Bc6QnnwaPLOMv3J',
    'Belgium': 'apVM8aZ8hKZFvnKm7',
    'Brazil': 'TyToNta7jGKkpszMZ',
    'Bulgaria': 'np4eYah8M5uQtj0Su',
    'Canada': 'fabbocwKrtxSDf96h',
    'China': 'x4iHxk7TVGI7UxFv6',
    'Czech_Republic': 'K373S4uCFR9W1K8ei',
    'Denmark': 'EAlpwScH29Qa5m60g',
    'Estonia': 'AZUhwS51lBBg26wSG',
    'Finland': 'jEFt5tgCTMfjJpLD3',
    'France': 'ufVgKLP8ljtn3ufaU',
    'Germany': 'OHrZyNo9BzT6xKMRD',
    'Hungary': 'RGEUeKe60NjU16Edo',
    'India': 'toDWvRj1JpTXiM8FF',
    'Iran': 'XV4DWf1ctkSPA8H99',
    'Italy': 'UFpnR8mukiu0TSrb4',
    'Japan': 'YbboJrL3cgVfkV1am',
    'Kosovo': 'C10heVVVE8yBd1YvF',
    'Lithuania': 'xhGDb8VTqjtm1AQL6',
    'Luxembourg': 'RVkUl1Y7FZn3Y410K',
    'Malaysia': '6t65lJVfs3d8s6aKc',
    'Netherlands': 'vqnEUe7VtKNMqGqFF',
    'Nigeria': 'Eb694wt67UxjdSGbc',
    'Norway': '3qlmMu1XN2ZLoVIQt',
    'Pakistan': 'QhfG8Kj6tVYMgud6R',
    'Palestine': 'SbribCOVf2wgR868y',
    'Philippines': 'lFItbkoNDXKeSWBBA',
    'Poland': '3Po6TV7wTht4vIEid',
    'Portugal': 'BXGEYTTUQzYBboEQK',
    'Romania': 'KUlj8EGfDGHiB0gU1',
    'Russia': '1brJ0NLbQaJKPTWMO',
    'Saudi_Arabia': '40xwYCZ57p5OkyBIJ',
    'Serbia': 'aHENGKUPUhKlX97aL',
    'Singapore': 'yaPbKe9e5Et61bl7W',
    'Slovakia': 'GlTLAdXAuOz6bLAIO',
    'Slovenia': '603AyvQ8QjyqmnZx6',
    'South_Korea': 'TMFbhs7qtXpGpeaeP',
    'Spain': 'lluBbYoQVN65R3BGO',
    'Sweden': '8mRFdwyukavRNCr42',
    'Switzerland': 'lDegAca820XgvjE0C',
    'Turkey': '28ljlt47S5XEd1qIi',
    'United_Kingdom': 'KWLojgM5r1JmMW4b4',
    'United_States': 'moxA3Q0aZh5LosewB',
    'Vietnam': 'EaCBL1JNntjR3EakU'
}

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

def get(url):
    try:
        res = requests.get(url)
        return res.json()
    except:
        return False

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
        
def matchingCountry(word):
    ans = ""
    score = 0
    for key in countries:
        if similar(word, key) > score:
            score = similar(word, key)
            ans = key
    return countries[ans]

@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    # print('received my event: ' + str(json))
    # socketio.emit('my response', json, callback=messageReceived)
    msg = {"user_name": "", "message": ""}
    if json["data"] == "User Connected":
        socketio.emit('my response', json, callback=messageReceived)
    elif json["data"] == "message":
        socketio.emit('my response', json, callback=messageReceived)
        resp = client.message(json["message"])
        print(resp)
        if resp['intents'][0]['name'] == "greeting":
            msg["user_name"] = "Steve"
            msg["message"] = "Hello there Human"
        elif resp['intents'][0]['name'] == "infected_get":
            msg["user_name"] = "Steve"
            code = matchingCountry(resp['entities']['country:country'][0]['body'])
            print(code)
            data = get("https://api.apify.com/v2/key-value-stores/" + code + "/records/LATEST?disableRedirect=true")
            if 'sourceUrl' in data:
                msg["message"] = 'The number of current infected patients are ' + str(data['infected']) + ' and the source is from ' + str(data['sourceUrl'])
            else:
                msg["message"] = 'The number of current infected patients are ' + str(data['infected'])
        elif resp['intents'][0]['name'] == "dead_get":
            print('hello')
            msg['user_name'] = 'Steve'
            code = matchingCountry(resp['entities']['country:country'][0]['body'])
            data = get("https://api.apify.com/v2/key-value-stores/" + code + "/records/LATEST?disableRedirect=true")
            if 'sourceUrl' in data:
                msg["message"] = 'The total number of deaths are ' + str(data['deceased']) + ' and the source is from ' + str(data['sourceUrl'])
            else:
                msg["message"] = 'The total number of deaths are ' + str(data['deceased'])
        socketio.emit('my response', msg, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
