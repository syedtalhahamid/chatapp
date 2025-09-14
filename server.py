from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

# Handle joining chat
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = 'main'
    join_room(room)
    send(f"{username} has entered the chat", room=room)

# Handle leaving chat
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = 'main'
    leave_room(room)
    send(f"{username} has left the chat", room=room)

# Handle sending message
@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, room='main')

if __name__ == '__main__':
    # Bind to 0.0.0.0 for Docker
    socketio.run(app, host="0.0.0.0", port=12345)
