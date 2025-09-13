from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# In-memory store for chat history (can be replaced with DB)
chat_rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    if room not in chat_rooms:
        chat_rooms[room] = []
    emit('chat_history', chat_rooms[room], room=request.sid)

@socketio.on('send_message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    timestamp = datetime.now().strftime('%H:%M')
    
    chat_entry = {'username': username, 'message': message, 'time': timestamp}
    
    # Store message
    if room not in chat_rooms:
        chat_rooms[room] = []
    chat_rooms[room].append(chat_entry)
    
    # Broadcast to room
    emit('receive_message', chat_entry, room=room)
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=12345)
