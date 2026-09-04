import requests
import time
import json

from datetime import datetime


def check_site(url):
  checked_at = datetime.now().isoformat(timespec="seconds")
  try:
    start = time.perf_counter()
    response = requests.get(url, timeout=5)
    end = time.perf_counter()
    response_time = end - start
    result = {
      "url": url,
      "available": 200<= response.status_code < 300,
      "status_code": response.status_code,
      "response_time": response_time,
      "error": None,
      "checked_at": checked_at
    }
    return result

  except requests.RequestException as error:
    result = {
    "url": url,
    "available": False,
    "status_code": None,
    "response_time": None,
    "error": str(error),
    "checked_at": checked_at
    }
    return result


def display_result(result):
  print(f"Сайт: {result['url']}")

  if result['available']:
    print("Статус: Доступен")
    print(f"HTTP: {result['status_code']}")
    print(f"Время ответа: {result['response_time']:.3f} сек.")
    print(f"Проверено: {result['checked_at']}")
  else:
    print("Статус: недоступен")
    print(f"Ошибка: {result['error']}")

def save_result(result):
  try:
    with open("history.json", "r", encoding="utf-8") as file:
      history = json.load(file)
  except FileNotFoundError:
    history = []
  history.append(result)
  with open("history.json", "w", encoding="utf-8") as file:
    json.dump(
      history,
      file,
      indent=4,
      ensure_ascii=False
      )


def main():
        
  sites = [
      "https://example.com",
      "https://python.org",
      "https://github.com"
  ]

  
  for site in sites:
    result = check_site(site)
    display_result(result)
    save_result(result)

if __name__ == "__main__":
  main()

