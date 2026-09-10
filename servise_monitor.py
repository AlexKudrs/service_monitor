import requests
import time
import json

from datetime import datetime

def load_config():
  try:
    with open("config.json","r", encoding="utf-8") as file:
      config = json.load(file)

    sites = config["sites"]
    if not isinstance(sites, list):
      print("Ошибка: sites должен быть списком")
      return None
    for site in sites:
      if not isinstance(site, str):
        print("Ошибка названия сайта")
        return None
      if not site.startswith(("http://", "https://")):
       print("Ошибка в названии сайта")
       return None

    return config
  except FileNotFoundError:
    print("Нет файла config.json")
    return None
  except json.JSONDecodeError:
    print("Ошибка чтения config.json")
    return None
  except KeyError:
    print("Ошибка чтения KEY")
    return None
   

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
  except json.JSONDecodeError:
    print("Ошибка файл 'history.json' поврежден")
    history = []
  history.append(result)
  with open("history.json", "w", encoding="utf-8") as file:
    json.dump(
      history,
      file,
      indent=4,
      ensure_ascii=False
      )

def load_history():
  try:
    with open("history.json", "r", encoding="utf-8") as file:
      history = json.load(file)
    return history
  except FileNotFoundError:
    return []
  except json.JSONDecodeError:
    print("Ошибка файл 'history.json' поврежден")
    return []

def calculate_statistics(history):
  total_checks = len(history)
  successful = 0
  response_count = 0
  total_response_time = 0

  for item in history:
    if item["available"]:
      successful += 1
    if item["response_time"] is not None:
      response_count += 1
      total_response_time += item["response_time"]

  failed = total_checks - successful

  if response_count > 0:
    average_response_time = total_response_time / response_count
  else:
    average_response_time = None
  
  if total_checks > 0:
    uptime = successful / total_checks * 100
  else:
    uptime = 0


  stats = {
    "total_checks": total_checks,
    "successful": successful,
    "failed": failed,
    "average_response_time": average_response_time,
    "uptime": uptime

  }

  return stats

def display_statistics(stats):
  print("=====Статистика====")
  print(f"Всего проверок:{stats['total_checks']}")
  print(f"Успешных: {stats['successful']}")
  print(f"Неудачных: {stats['failed']}")
  print(f"Uptime {stats['uptime']:.2f}%")

  if stats["average_response_time"] is not None:
        print(
            f"Среднее время ответа: "
            f"{stats['average_response_time']:.3f} сек."
        )
  else:
      print("Среднее время ответа: нет данных")

def main():
        
  config = load_config()
  if config is None:
    return
  sites = config["sites"]
  check_interval = config["check_interval"]
  try:
    while True:
      for site in sites:
        result = check_site(site)
        display_result(result)
        save_result(result)
      history = load_history()
      stats = calculate_statistics(history)

      display_statistics(stats)
      time.sleep(check_interval)
  except KeyboardInterrupt:
    print("\nService monitor остановлен")

if __name__ == "__main__":
  main()

