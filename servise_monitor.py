import requests

url = "https://example.com"
try:
  response = requests.get(url, timeout=5)

  if 200 <= response.status_code < 300:
    print("Сайт доступен")
  else:
    print("Сайт ответил с ошибкой")
  print('HTTP-код:',response.status_code)
except requests.RequestException as error:
  print('НЕ удалось подключится к сайту')
  print('Причина,', error)