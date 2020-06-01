# from flask import Flask, render_template
# from flask_socketio import SocketIO
# from wit import Wit

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
# socketio = SocketIO(app)
# client = Wit("2XWTIKVOL6RTJLGCQQ7OXDG6YQVBCTMH")


# @app.route('/')
# def sessions():
#     return render_template('session.html')

# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!')

# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     # print('received my event: ' + str(json))
#     # socketio.emit('my response', json, callback=messageReceived)
#     msg = {"user_name": "", "message": "", "bot_name": "Steve", "bot_message": ""}
#     if json["data"] == "User Connected":
#         socketio.emit('my response', json, callback=messageReceived)
#     elif json["data"] == "message":
#         resp = client.message(json["message"])
#         if resp['intents'][0]['name'] == "greeting":
#             msg["user_name"] = json["user_name"]
#             msg["message"] = json["message"]
#             msg["bot_message"] = "Hello there Human"
#         elif resp['intents'][0]['name'] == "temperature":
#             msg["user_name"] = json["user_name"]
#             msg["message"] = json["message"]
#             msg["bot_message"] = "I don't know but it's hot"
#         socketio.emit('my response', msg, callback=messageReceived)

# if __name__ == '__main__':
#     socketio.run(app, debug=True)


from flask import Flask, render_template
from flask_socketio import SocketIO
from wit import Wit
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
client = Wit("2XWTIKVOL6RTJLGCQQ7OXDG6YQVBCTMH")


@app.route('/')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

def get(url):
    try:
        res = requests.get(url)
        return res.json()
    except:
        return False

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
        if resp['intents'][0]['name'] == "greeting":
            msg["user_name"] = "Steve"
            msg["message"] = "Hello there Human"
        elif resp['intents'][0]['name'] == "infected_get":
            msg["user_name"] = "Steve"
            data = get("https://api.apify.com/v2/key-value-stores/pp4Wo2slUJ78ZnaAi/records/LATEST?disableRedirect=true")
            msg["message"] = str(data['infected'])
        socketio.emit('my response', msg, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)


