from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('mensaje')
def handle_mensaje(data):
    if 'mensaje' not in data or not data['mensaje']:
        emit('mensaje', {'username': 'Error', 'mensaje': 'Mensaje vacío o mal formado.'})
        return
    if 'username' in data:
        username = data['username']
    else:
        username = 'Anónimo'
    message = data['mensaje']
    emit('mensaje', {'username': username, 'mensaje': message}, broadcast=True)
