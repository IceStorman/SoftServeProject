from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

connected_users = {}

@socketio.on("connect")
def handle_connect():
    print("A user connected")

@socketio.on("register")
def register_user(data):
    user_id = data.get("user_id")
    if user_id:
        connected_users[user_id] = True
        print(f"User {user_id} registered for recommendations")

def send_recommendations(user_id, recommendations):
    if user_id in connected_users:
        socketio.emit(f"recommendations_{user_id}", recommendations)

