from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


# Funkce pro zpracování události z GitHub webhooku
@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.json
    # Zjistění typu události
    event_type = request.headers.get('X-GitHub-Event')

    # Reakce na událost typu "push" (změna kódu)
    if event_type == 'push':
        handle_push_event(data)

    return jsonify({'message': 'Received'}), 200


# Funkce pro zpracování události "push"
def handle_push_event(data):
    bot_token = '6972789464:AAFZfAKYnLyjcpaZIGJFQ0yOvY3zLlA1K00'
    chat_id = '#-4106251145'
    message = 'Something happened in your repository!'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print('Chyba při odesílání zprávy do Telegramu:', response.text)


if __name__ == '__main__':
    app.run(debug=True)
