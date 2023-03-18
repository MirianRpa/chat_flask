from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins='*')


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('mensaje')
async def handle_mensaje(data):
    if 'mensaje' not in data or not data['mensaje']:
        emit('mensaje', {'username': 'Error', 'mensaje': 'Mensaje vacío o mal formado.'})
        return
    if 'username' in data:
        username = data['username']
    else:
        username = 'Anónimo'
    message = data['mensaje']
    await socketio.emit('mensaje', {'username': username, 'mensaje': message}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
