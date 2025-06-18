import streamlit as st
import itertools
import heapq
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import time

st.set_page_config(layout="wide")

def generate_runtime_plot(results):
    alg_names = []
    runtimes = []

    for idx in sorted(results.keys()):
        _, _, _, _, elapsed_time, error = results[idx]
        alg = st.session_state.get(f"alg_{idx}", f"Algorytm {idx+1}")
        if elapsed_time is not None and not error:
            alg_names.append(alg)
            runtimes.append(elapsed_time)

    if not alg_names:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(alg_names, runtimes, color='skyblue')
    ax.set_xlabel("Czas obliczeń (s)")
    ax.set_title("Porównanie czasów obliczeń algorytmów")
    return fig

# --- Algorytmy ---
def johnson_algorithm(jobs):
    if not jobs or any(len(job) != 2 for job in jobs):
        raise ValueError("Algorytm Johnsona wymaga dokładnie 2 maszyn dla każdego zadania.")
    n = len(jobs)
    left, right = [], []
    indexed_jobs = list(enumerate(jobs))
    while indexed_jobs:
        min_index, (min_a, min_b) = min(indexed_jobs, key=lambda x: min(x[1][0], x[1][1]))
        if min_a <= min_b:
            left.append(min_index)
        else:
            right.insert(0, min_index)
        indexed_jobs.remove((min_index, (min_a, min_b)))
    return left + right

def calculate_makespan(order, jobs):
    n, m = len(order), len(jobs[0])
    start = [[0] * n for _ in range(m)]
    end = [[0] * n for _ in range(m)]
    for j in range(n):
        job_index = order[j]
        for i in range(m):
            if i == 0 and j == 0:
                start[i][j] = 0
            elif i == 0:
                start[i][j] = end[i][j - 1]
            elif j == 0:
                start[i][j] = end[i - 1][j]
            else:
                start[i][j] = max(end[i - 1][j], end[i][j - 1])
            end[i][j] = start[i][j] + jobs[job_index][i]
    return end[-1][-1], start, end

def lomnicki_algorithm(jobs):
    best_order, best_makespan = [], float('inf')
    for perm in itertools.permutations(range(len(jobs))):
        makespan, _, _ = calculate_makespan(perm, jobs)
        if makespan < best_makespan:
            best_makespan = makespan
            best_order = perm
    return list(best_order), best_makespan

def brown_lomnicki_algorithm(jobs):
    if not jobs or any(len(job) != 3 for job in jobs):
        raise ValueError("Algorytm Brown-Łomnicki wymaga dokładnie 3 maszyn dla każdego zadania.")
    UB, best_order = float('inf'), []
    heap = [(0, [i]) for i in range(len(jobs))]
    heapq.heapify(heap)
    while heap:
        _, partial = heapq.heappop(heap)
        remaining = [j for j in range(len(jobs)) if j not in partial]
        if not remaining:
            makespan, _, _ = calculate_makespan(partial, jobs)
            if makespan < UB:
                UB = makespan
                best_order = partial
        else:
            for idx in range(len(partial)):
                j = partial[idx]
                if idx == 0:
                    s1, s2, s3 = jobs[j][0], jobs[j][0] + jobs[j][1], jobs[j][0] + jobs[j][1] + jobs[j][2]
                else:
                    s1 += jobs[j][0]
                    s2 = max(s1, s2) + jobs[j][1]
                    s3 = max(s2, s3) + jobs[j][2]
            tk1, tk2, tk3 = s1, s2, s3
            sum_t1 = sum(jobs[j][0] for j in remaining)
            sum_t2 = sum(jobs[j][1] for j in remaining)
            sum_t3 = sum(jobs[j][2] for j in remaining)
            min_t2_3 = min((jobs[j][1] + jobs[j][2]) for j in remaining)
            min_t3 = min(jobs[j][2] for j in remaining)
            phi = max(tk1 + sum_t1 + min_t2_3, tk2 + sum_t2 + min_t3, tk3 + sum_t3)
            if phi < UB:
                for j in remaining:
                    heapq.heappush(heap, (phi, partial + [j]))
    return best_order, UB

def brute_force_algorithm(jobs):
    best_order, best_makespan, best_start = [], float('inf'), None
    johnson = johnson_algorithm(jobs) if len(jobs[0]) == 2 else None
    for perm in itertools.permutations(range(len(jobs))):
        makespan, start, _ = calculate_makespan(perm, jobs)
        if makespan < best_makespan:
            best_makespan = makespan
            best_order = perm
            best_start = start
        elif makespan == best_makespan and johnson and list(perm) == johnson:
            best_order = perm
            best_start = start
    return list(best_order), best_makespan, best_start

def plot_gantt(order, jobs, start, ax):
    machines = len(jobs[0])
    for j, job_id in enumerate(order):
        for m in range(machines):
            ax.broken_barh([(start[m][j], jobs[job_id][m])], (m - 0.4, 0.8), facecolors=f"C{j}")
            ax.text(start[m][j] + jobs[job_id][m] / 2, m, str(job_id + 1), va='center', ha='center', color='white', fontsize=9)
    ax.set_yticks(range(machines))
    ax.set_yticklabels([f"Maszyna {i+1}" for i in range(machines)])
    ax.set_xlabel("Czas")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

def show_jobs_table(jobs):
    df = pd.DataFrame(jobs, columns=[f"Maszyna {i+1}" for i in range(len(jobs[0]))])
    df.index = [f"Zadanie {i+1}" for i in range(len(jobs))]
    st.table(df)

def show_order_chart(order, ax):
    bars = [str(i+1) for i in order]
    sns.heatmap([order], annot=[bars], cbar=False, fmt="", cmap="Blues", linewidths=1, linecolor='gray', xticklabels=False, yticklabels=False, ax=ax)
    ax.set_title("Optymalna kolejność zadań")

# --- Stan aplikacji ---
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'columns_count' not in st.session_state:
    st.session_state.columns_count = 1
if 'jobs_data' not in st.session_state:
    st.session_state.jobs_data = []
if 'machines_count' not in st.session_state:
    st.session_state.machines_count = 3
if 'jobs_generated' not in st.session_state:
    st.session_state.jobs_generated = False

st.title("Algorytmy szeregowania zadań")

# Sekcja danych wejściowych
st.header("Dane wejściowe")
n_tasks = st.number_input("Liczba zadań", min_value=2, max_value=10, value=4)
m_brygady = st.selectbox("Liczba maszyn", options=[2, 3], index=1)
manual_input = st.checkbox("Wprowadź czasy ręcznie")

jobs = []
if manual_input:
    st.session_state.jobs_generated = False
    st.write("Wprowadź czasy zadań:")
    for i in range(n_tasks):
        cols_inner = st.columns(m_brygady)
        job = [cols_inner[m].number_input(f"Zadanie {i+1}, Maszyna {m+1}", min_value=1, value=3, key=f"input_{i}_{m}") for m in range(m_brygady)]
        jobs.append(tuple(job))
    st.session_state.jobs_data = jobs
else:
    if not st.session_state.jobs_generated:
        st.session_state.jobs_data = [tuple(random.randint(1, 6) for _ in range(m_brygady)) for _ in range(n_tasks)]
        st.session_state.jobs_generated = True

st.session_state.machines_count = m_brygady

if st.button("🪩 Wyczyść sesję wyników"):
    st.session_state.results = {}
    st.session_state.jobs_generated = False

col_buttons = st.columns([1, 1])
if col_buttons[0].button("➕ Dodaj kolumnę"):
    st.session_state.columns_count += 1
if col_buttons[1].button("➖ Usuń kolumnę"):
    st.session_state.columns_count = max(1, st.session_state.columns_count - 1)

if st.button("▶️ Uruchom wszystkie algorytmy"):
    for idx in range(st.session_state.columns_count):
        jobs = st.session_state.jobs_data
        m_brygady = st.session_state.machines_count
        selected_algorithm = st.session_state.get(f"alg_{idx}", "Johnson")

        if selected_algorithm == "Johnson" and m_brygady != 2:
            st.session_state.results[idx] = (jobs, [], 0, [], None, "Błąd: Algorytm Johnsona działa tylko dla 2 maszyn.")
        elif selected_algorithm not in ["Johnson", "Brute Force"] and m_brygady == 2:
            st.session_state.results[idx] = (jobs, [], 0, [], None, "Błąd: Przy 2 maszynach dostępne są tylko algorytmy Johnsona i Brute Force.")
        else:
            try:
                start_time = time.time()
                if selected_algorithm == "Johnson":
                    order = johnson_algorithm(jobs)
                    time_exec, start, _ = calculate_makespan(order, jobs)
                elif selected_algorithm == "Łomnicki":
                    order, time_exec = lomnicki_algorithm(jobs)
                    _, start, _ = calculate_makespan(order, jobs)
                elif selected_algorithm == "Brown-Łomnicki":
                    order, time_exec = brown_lomnicki_algorithm(jobs)
                    _, start, _ = calculate_makespan(order, jobs)
                elif selected_algorithm == "Brute Force":
                    order, time_exec, start = brute_force_algorithm(jobs)
                elapsed_time = time.time() - start_time
                st.session_state.results[idx] = (jobs, order, time_exec, start, elapsed_time, None)
            except Exception as e:
                st.session_state.results[idx] = (jobs, [], 0, [], None, f"Błąd wewnętrzny: {str(e)}")

cols = st.columns(st.session_state.columns_count)

for idx, col in enumerate(cols):
    with col:
        st.subheader(f"Numer {idx+1}")
        selected_algorithm = st.selectbox("Wybierz algorytm", options=["Johnson", "Łomnicki", "Brown-Łomnicki", "Brute Force"], key=f"alg_{idx}")
        if idx in st.session_state.results:
            jobs, order, time_exec, start, elapsed_time, error = st.session_state.results[idx]
            if error:
                st.error(error)
            else:
                st.subheader("Czasy wykonania zadań")
                show_jobs_table(jobs)
                st.subheader("Optymalna kolejność")
                fig, ax = plt.subplots(figsize=(8, 1))
                show_order_chart(order, ax)
                st.pyplot(fig)
                st.write("Czas wykonania:", time_exec)
                if elapsed_time is not None:
                    st.write(f"Czas obliczeń algorytmu: {elapsed_time:.8f} sekundy")
                fig, ax = plt.subplots(figsize=(10, 3))
                plot_gantt(order, jobs, start, ax)
                st.pyplot(fig)


# --- Wykres czasów obliczeń ---
st.header("Porównanie czasów obliczeń algorytmów")
fig_runtime = generate_runtime_plot(st.session_state.results)
if fig_runtime:
    st.pyplot(fig_runtime)
else:
    st.info("Brak danych do wyświetlenia wykresu czasów obliczeń.")
