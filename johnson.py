#!/usr/bin/env python3

def johnsons_algorithm(tasks):
    """
    tasks: lista krotek (task_name, time_on_machine1, time_on_machine2)
    zwraca: uporządkowaną listę zadań według algorytmu Johnsona
    """
    left = []
    right = []

    for task in tasks:
        name, m1, m2 = task
        if m1 <= m2:
            left.append((m1, task))
        else:
            right.append((m2, task))

    left.sort()   # rosnąco po czasie na M1
    right.sort(reverse=True)  # malejąco po czasie na M2

    sorted_tasks = [t[1] for t in left + right]
    return sorted_tasks

def print_schedule(schedule):
    print("Zalecana kolejność zadań:")
    for i, task in enumerate(schedule, 1):
        name, m1, m2 = task
        print(f"{i}. {name} (M1: {m1}, M2: {m2})")

# Przykład użycia
if __name__ == "__main__":
    # (nazwa_zadania, czas_na_maszynie1, czas_na_maszynie2)
    tasks = [
        ("Zadanie A", 3, 8),
        ("Zadanie B", 12, 4),
        ("Zadanie C", 6, 5),
        ("Zadanie D", 2, 7),
        ("Zadanie E", 9, 3)
    ]

    schedule = johnsons_algorithm(tasks)
    print_schedule(schedule)
