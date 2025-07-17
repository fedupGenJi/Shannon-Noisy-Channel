from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def noisy_channel(data):
    if not data:
        return data

    data_list = list(data)
    length = len(data_list)

    percentage = random.uniform(0.01, 0.8)
    print("Error Perdentage:",percentage)
    num_changes = max(1, (length * percentage) // 100)

    modified_indices = set()

    for _ in range(num_changes):
        idx = random.randint(0, length - 1)
        while idx in modified_indices:
            idx = random.randint(0, length - 1)

        modified_indices.add(idx)

        original_char = data_list[idx]
        base64_chars = string.ascii_letters + string.digits + '+/='
        new_char = random.choice(base64_chars.replace(original_char, ''))

        data_list[idx] = new_char

    return ''.join(data_list)

@app.route('/sender')
def screen_a():
    return render_template('sender.html')

@app.route('/receiver')
def screen_b():
    return render_template('receiver.html')

@socketio.on('send_message')
def handle_message(data):
    print(f"Received message from A: {data}")
    emit('receive_message', data, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    print("Encrypted message received:", data)
    noisy_data = noisy_channel(data)
    print("Corrupted (noisy) data:", noisy_data)

    socketio.emit('receive_message', noisy_data)

if __name__ == '__main__':
    socketio.run(app, debug=True, port='6789')