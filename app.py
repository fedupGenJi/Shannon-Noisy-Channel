from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/screen-a')
def screen_a():
    return render_template('sender.html')

@app.route('/screen-b')
def screen_b():
    return render_template('receiver.html')

@socketio.on('send_message')
def handle_message(data):
    print(f"Received message from A: {data}")
    emit('receive_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port='6789')
