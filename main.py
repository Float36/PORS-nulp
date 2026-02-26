import random
import time
import json
import threading



def selection_sort(arr: list[int]) -> list[int]:
    """Сортування вибором"""
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def merge(left_arr: list[int], right_arr: list[int]) -> list[int]:
    """Злиття двох відсортованих списків"""
    result = []
    i = j = 0
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] < right_arr[j]:
            result.append(left_arr[i])
            i += 1
        else:
            result.append(right_arr[j])
            j += 1
    result.extend(left_arr[i:])
    result.extend(right_arr[j:])

    return result


def sequential_chunks_sort(arr: list[int], num_chunks=4) -> list[int]:
    """Сортування частинами послідовно (в одному потоці)"""
    if num_chunks < 2:
        return selection_sort(arr)

    size = len(arr) // num_chunks
    chunks = [arr[i * size: (i + 1) * size] for i in range(num_chunks)]
    chunks[-1].extend(arr[num_chunks * size:])

    sorted_chunks = []
    for chunk in chunks:
        sorted_chunks.append(selection_sort(chunk))

    final_result = sorted_chunks[0]
    for i in range(1, num_chunks):
        final_result = merge(final_result, sorted_chunks[i])

    return final_result

def threaded_selection_sort(arr: list[int], num_threads=2) -> list[int]:
    """Паралельне сортування (Поділ, сортування, злиття)"""
    if num_threads < 2:
        return selection_sort(arr)

    size = len(arr) // num_threads
    chunks = [arr[i * size : (i + 1) * size] for i in range(num_threads)]

    chunks[-1].extend(arr[num_threads * size: ])

    threads = []
    results = [None] * num_threads

    def worker(idx: int, data: list[int]):
        results[idx] = selection_sort(data)

    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i, chunks[i]))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    final_result = results[0]
    for i in range(1, num_threads):
        final_result = merge(final_result, results[i])

    return final_result



# Робота з даними
def generate_data(size, filename="input_data.json"):
    data = [random.randint(-100000, 100000) for _ in range(size)]
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"Згенеровано {size} елементів у файл {filename}")

def load_data(filename="input_data.json"):
    with open(filename, 'r') as f:
        return json.load(f)

def save_output(data, filename="output_data.json"):
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"Результат збережено у {filename}")



# Функція для запуску
def run_experiment(size):
    generate_data(size)  # Генеруємо дані один раз
    data = load_data()

    # 1. Послідовно (повний масив) - виконуємо ОДИН раз для бази порівняння
    data_seq = data.copy()
    start = time.perf_counter()
    selection_sort(data_seq)
    time_full_seq = time.perf_counter() - start
    print(f"Послідовно (1 потік): {time_full_seq:.4f} сек")

    # Список кількості потоків для тестування
    thread_counts = [2, 4, 8, 64]

    for n in thread_counts:
        print(f"\n>>> ТЕСТ ДЛЯ {n} ПОТОКІВ / ЧАСТИН:")

        # 2. Послідовно (частинами)
        data_chunks_seq = data.copy()
        start = time.perf_counter()
        sequential_chunks_sort(data_chunks_seq, num_chunks=n)
        time_chunks_seq = time.perf_counter() - start
        print(f"2. Частинами послідовно ({n} частини, 1 потік): {time_chunks_seq:.4f} сек")

        # 3. Паралельно (потоками)
        data_par = data.copy()
        start = time.perf_counter()
        result_par = threaded_selection_sort(data_par, num_threads=n)
        time_threaded = time.perf_counter() - start
        print(f"3. Частинами в потоках ({n} частини, {n} потоки): {time_threaded:.4f} сек")

        # АНАЛІЗ для поточної кількості потоків
        alg_gain = time_full_seq / time_chunks_seq
        hw_gain = time_chunks_seq / time_threaded
        total_gain = time_full_seq / time_threaded

        print(f"   - Алгоритмічний приріст: {alg_gain:.2f}x")
        print(f"   - Апаратний приріст: {hw_gain:.2f}x")
        print(f"   - ЗАГАЛЬНЕ ПРИСКОРЕННЯ: {total_gain:.2f}x")

    save_output(data_par)


if __name__ == "__main__":
    N = 30000
    run_experiment(N)