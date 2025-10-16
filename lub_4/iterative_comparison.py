import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

@lru_cache(1024)
def cached_fact_iterative(n: int) -> int:
    """Кешированный итеративный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def uncached_fact_iterative(n: int) -> int:
    """Некешированный итеративный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def benchmark(func, n, number=1, repeat=5):
    def setup():
        """Функция setup для timeit - очищает кеш перед каждым повторением"""
        if hasattr(func, 'cache_clear'):
            func.cache_clear()
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n),setup=setup, number=number, repeat=repeat)
    return min(times)

def main():
    # фиксированный набор данных
    test_data = list(range(10, 900, 10))
    cech_iterative = []
    uncech_iterative = []
    for n in test_data:
      cech_iterative.append(benchmark(cached_fact_iterative, n))
      uncech_iterative.append(benchmark(uncached_fact_iterative, n))
    # Визуализация
    plt.plot(test_data, cech_iterative, label="Кешированный итеративный ")
    plt.plot(test_data, uncech_iterative, label="Итеративный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение кешированного итеративного и итеративного факториалов")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
