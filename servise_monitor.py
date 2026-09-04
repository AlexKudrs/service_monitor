import requests
import time



def check_site(url):
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
      "error": None
    }
    return result

  except requests.RequestException as error:
    result = {
    "url": url,
    "available": False,
    "status_code": None,
    "response_time": None,
    "error": str(error)
    }
    return result


def display_result(result):
  print(f"Сайт: {result['url']}")

  if result['available']:
    print("Статус: Доступен")
    print(f"HTTP: {result['status_code']}")
    print(f"Время ответа: {result['response_time']:.3f} сек.")
  else:
    print("Статус: недоступен")
    print(f"Ошибка: {result['error']}")

def main():
        
  sites = [
      "https://example.com",
      "https://python.org",
      "https://github.com"
  ]

  
  for site in sites:
    result = check_site(site)
    display_result(result)

if __name__ == "__main__":
  main()

