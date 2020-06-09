from flask import Flask, render_template
from flask_socketio import SocketIO
from wit import Wit
from difflib import SequenceMatcher
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
# socketio = SocketIO(app, cors_allowed_origins='*')
socketio = SocketIO(app)
client = Wit("2XWTIKVOL6RTJLGCQQ7OXDG6YQVBCTMH")

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

def matchinCountry2(word, arr):
    ans = 0
    score = 0
    for i in range(len(arr)):
        if similar(word, arr[i]["Country"]) > score:
            score = similar(word, arr[i]["Country"])
            ans = i
    return arr[ans]

def findCountry(country, countries):
    pass


@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    # print('received my event: ' + str(json))
    # socketio.emit('my response', json, callback=messageReceived)
    msg = {"user_name": "", "message": "", "data": [], "labels": []}
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
            data = get("https://api.covid19api.com/summary")
            arr = data["Countries"]
            ans = matchinCountry2(resp['entities']['country:country'][0]['value'], arr)
            msg["message"] = "The number of new confirmed cases in " + ans["Country"] + " is " + str(ans["NewConfirmed"])

        elif resp['intents'][0]['name'] == "dead_get":
            msg["user_name"] = "Steve"
            data = get("https://api.covid19api.com/summary")
            arr = data["Countries"]
            ans = matchinCountry2(resp['entities']['country:country'][0]['value'], arr)
            msg["message"] = "The number of new confirmed deaths in " + ans["Country"] + " is " + str(ans["NewDeaths"])

        elif resp['intents'][0]['name'] == "recoveries_get":
            msg["user_name"] = "Steve"
            data = get("https://api.covid19api.com/summary")
            arr = data["Countries"]
            ans = matchinCountry2(resp['entities']['country:country'][0]['value'], arr)
            msg["message"] = "The number of new confirmed recoveries in " + ans["Country"] + " is " + str(ans["NewRecovered"])

        elif resp['intents'][0]['name'] == "infected_total_get":
            msg["user_name"] = "Steve"
            data = get("https://api.covid19api.com/summary")
            arr = data["Countries"]
            ans = matchinCountry2(resp['entities']['country:country'][0]['value'], arr)
            msg["message"] = "The number of total confirmed infected cases in " + ans["Country"] + " is " + str(ans["TotalConfirmed"])
        elif resp['intents'][0]['name'] == "dead_total_get":
            msg["user_name"] = "Steve"
            data = get("https://api.covid19api.com/summary")
            arr = data["Countries"]
            ans = matchinCountry2(resp['entities']['country:country'][0]['value'], arr)
            msg["message"] = "The number of total confirmed dead cases in " + ans["Country"] + " is " + str(ans["TotalDeaths"])
        elif resp['intents'][0]['name'] == "recoveries_total_get":
            msg["user_name"] = "Steve"
            data = get("https://api.covid19api.com/summary")
            arr = data["Countries"]
            ans = matchinCountry2(resp['entities']['country:country'][0]['value'], arr)
            msg["message"] = "The number of total confirmed recovered cases in " + ans["Country"] + " is " + str(ans["TotalRecovered"])
        elif resp['intents'][0]['name'] == "graph_get":
            msg["user_name"] = "Steve"
            data = get("https://api.covid19api.com/summary")
            arr = data["Countries"]
            ans = matchinCountry2(resp['entities']['country:country'][0]['value'], arr)
            slug = ans["Slug"]
            timedata = get("https://api.covid19api.com/total/dayone/country/" + slug)
            if 'status:Recovered' in resp['entities']:
                for i in range(len(timedata)):
                    msg["data"].append(timedata[i]['Recovered'])
                    msg["labels"].append('1')
            elif 'status:Confirmed' in resp['entities']:
                for i in range(len(timedata)):
                    msg["data"].append(timedata[i]['Confirmed'])
                    msg["labels"].append('1')
            elif 'status:Deaths' in resp['entities']:
                for i in range(len(timedata)):
                    msg["data"].append(timedata[i]['Deaths'])
                    msg["labels"].append('1')
            msg["message"] = "Data Stored"
        socketio.emit('my response', msg, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
