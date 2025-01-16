import time
import re
from collections import defaultdict
from hyperloglog import HyperLogLog
import pandas as pd


def load_log_file(file_path):
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    ip_addresses = []
    total_lines = 0
    with open(file_path, "r") as file:
        for line in file:
            total_lines += 1
            match = ip_pattern.search(line)
            if match:
                ip_addresses.append(match.group())
    print(f"Загальна кількість рядків у файлі: {total_lines}")
    print(f"Кількість знайдених IP-адрес: {len(ip_addresses)}")
    return ip_addresses


def count_unique_exact(ip_addresses):
    """Точний підрахунок унікальних IP-адрес за допомогою set."""
    return len(set(ip_addresses))


def count_unique_hyperloglog(ip_addresses, precision=0.01):
    # Підрахунок унікальних IP-адрес за допомогою HyperLogLog
    hll = HyperLogLog(precision)
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


def analyze_ip_frequencies(ip_addresses):
    # Аналізує частоту появи кожної IP-адреси
    frequency = defaultdict(int)
    for ip in ip_addresses:
        frequency[ip] += 1
    sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    print(f"Топ 10 найчастіших IP-адрес:")
    for ip, count in sorted_frequency[:10]:
        print(f"{ip}: {count} разів")
    return frequency


def compare_methods(file_path):
    ip_addresses = load_log_file(file_path)
    ip_frequencies = analyze_ip_frequencies(ip_addresses)

    # Точний підрахунок
    start_time = time.time()
    exact_count = count_unique_exact(ip_addresses)
    exact_time = time.time() - start_time

    # HyperLogLog підрахунок
    start_time = time.time()
    hll_count = count_unique_hyperloglog(ip_addresses)
    hll_time = time.time() - start_time

    # Порівняння результатів
    data = {
        "Метод": ["Точний підрахунок", "HyperLogLog"],
        "Унікальні елементи": [exact_count, hll_count],
        "Час виконання (сек.)": [exact_time, hll_time],
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    file_path = "lms-stage-access.log"

    results = compare_methods(file_path)

    print("Результати порівняння:")
    print(results.to_string(index=False))
