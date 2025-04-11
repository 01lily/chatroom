from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256
import base64
import spacy
import os
from spacy.cli import download # BUG FIX

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Load spaCy model
#nlp = spacy.load("en_core_web_sm") ORIGINAL LINE // BUG FIX

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# In-memory user session tracking
users = {}

def check_sentiment(message):
    doc = nlp(message)
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        if token.text.lower() in ['hate', 'kill', 'abuse', 'stupid']:
            return False
    return True

@socketio.on('join')
def handle_join(data):
    username = data['username']
    users[request.sid] = username
    emit('status', {'msg': f"{username} has joined the chat."}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    message = data['message']
    username = users.get(request.sid, "Anonymous")
    if not check_sentiment(message):
        emit('warning', {'msg': "Your message may contain harmful content."})
        return
    emit('message', {'msg': f"{username}: {message}"}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, "Anonymous")
    emit('status', {'msg': f"{username} has left the chat."}, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, broadcast=True, include_self=False)

@socketio.on('stopTyping')
def handle_stop_typing():
    emit('stopTyping', broadcast=True, include_self=False)



if __name__ == '__main__':
    socketio.run(app, debug=True)
