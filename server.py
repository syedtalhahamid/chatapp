from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    users[request.sid] = username
    emit('user_joined', {'username': username}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    username = users.get(request.sid, "Anonymous")
    message = data['message']
    emit('receive_message', {'username': username, 'message': message}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, "Anonymous")
    emit('user_left', {'username': username}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=12345)
