import requests

bot_token = '6972789464:AAFZfAKYnLyjcpaZIGJFQ0yOvY3zLlA1K00'
chat_id = '-4106251145'
message = 'Task done! :P'

url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
data = {'chat_id': chat_id, 'text': message}

response = requests.post(url, data=data)
print(response.json())
