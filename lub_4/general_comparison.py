import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

@lru_cache()
def cached_fact_recursive(n: int) -> int:
    """Кешированный рекурсивый факториал"""
    if n == 0:
        return 1
    return n * cached_fact_recursive(n - 1)

@lru_cache()
def cached_fact_iterative(n: int) -> int:
    """Кешированный итеративный факториал"""
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
    test_data = list(range(10, 300, 10))

    res_recursive = []
    res_iterative = []

    for n in test_data:
      res_recursive.append(benchmark(cached_fact_recursive, n))
      res_iterative.append(benchmark(cached_fact_iterative, n))

    # Визуализация
    plt.plot(test_data, res_recursive, label="Кешируемый рекурсивный")
    plt.plot(test_data, res_iterative, label="Кешируемый итеративный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение кешированных рекурсивного и итеративного факториалов")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
