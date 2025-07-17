from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from collections import Counter
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

def shannon_channel(data):
    if not data:
        return data

    encoded_data = ''.join(char * 5 for char in data)

    data_list = list(encoded_data)
    length = len(data_list)

    percentage = random.uniform(10, 45)
    print("Error Percentage (Shannon Slow):", percentage)
    num_changes = max(1, int((length * percentage) / 100))

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

    corrected_data = ''
    for i in range(0, len(data_list), 5):
        group = data_list[i:i+5]
        if not group:
            continue
        most_common = Counter(group).most_common(1)[0][0]
        corrected_data += most_common

    return corrected_data

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
    # noisy_data = noisy_channel(data)
    noisy_data = shannon_channel(data)
    print("Corrupted (noisy) data:", noisy_data)

    socketio.emit('receive_message', noisy_data)

if __name__ == '__main__':
    socketio.run(app, debug=True, port='6789')