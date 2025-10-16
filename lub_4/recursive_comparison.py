import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

@lru_cache(1024)
def cached_fact_recursive(n: int) -> int:
    """Кешированный рекурсивый факториал"""
    if n == 0:
        return 1
    return n * cached_fact_recursive(n - 1)

def uncached_fact_recursive(n: int) -> int:
    """Некешированный рекурсивый факториал"""
    if n == 0:
        return 1
    return n * uncached_fact_recursive(n - 1)


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

    ceh_recursive = []
    unceh_recursive = []

    for n in test_data:
      ceh_recursive.append(benchmark(cached_fact_recursive, n))
      unceh_recursive.append(benchmark(uncached_fact_recursive, n))

    # Визуализация
    plt.plot(test_data, ceh_recursive, label="Кешированный рекурсивный факториал")
    plt.plot(test_data, unceh_recursive, label="Рекурсивный факториал")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение кешированного рекурсивного и рекурсивного факториалов")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

