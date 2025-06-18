# TaskScheduling


Szeregowanie zadań

- Algorytm Johnsona
- Algorytm Łomnickiego
- Algorytm Browna-Łomnickiego (opcjonalnie)

max 18 pkt: Należy przeanalizować wybrany problem przy pomocy algorytmu Johnsona (mogą być same obliczenia).

max 26 pkt: To co wyżej + brute force + implementacja algorytmu Johnsona. Zestawić na wykresie porównanie otrzymanych wyników.

max 36 pkt: To co wyżej + algorytm Łomnickiego lub Browna-Łomnickiego. Zestawić na wykresie porównanie wyników oraz porównanie czasu wykonywania obliczeń dla różnych problemów.


## TODO - prezentacja:
- [X] Co to jest szeregowanie zadań
- [X] Example problem
- [X] problem do analizy? (obliczenia?)
- [X] Brute force + złożonośc
- [ ] Johnson + złożonośc + matma
- [ ] Lomnicki + złożoność + matma
- [ ] Brown-Lomnicki + złożoność + matma
- [ ] Implementacja algorytmów
- [ ] ~~Problem z prezentacji Bednarza (w screenach działania? - dla porównania dla Bednarza)~~
- [ ] Wykresy z porównaniem czasu wykonywania obliczeń
- [ ] Wykresy - porównanie wyników - różne problemy (demo)
- [ ] Wykresy - porównanie czasu wykonywania obliczeń algorytmów (demo)

### Prezentacja order
1. Co to jest szeregowanie zadań i na czym polega
2. Example problem

W fabryce produkowane są metalowe elementy. Każdy element musi przejść przez trzy etapy obróbki:

- Cięcie (Maszyna 1)
- Szlifowanie (Maszyna 2)
- Malowanie (Maszyna 3)

Maszyny mogą obsługiwać tylko jedno zlecenie na raz i każdy etap trwa inną ilość czasu dla każdego elementu.
Celem jest ustalenie kolejności produkcji, tak aby wszystkie elementy zostały wykonane w możliwie najkrótszym czasie.

| Część | Cięcie | Szlifowanie | Malowanie |
| ----- | ------ | ----------- | --------- |
| A     | 4 min  | 6 min       | 3 min     |
| B     | 2 min  | 7 min       | 4 min     |
| C     | 5 min  | 4 min       | 2 min     |
| D     | 3 min  | 5 min       | 5 min     |

Ustalić kolejność części A, B, C, D w taki sposób, aby zminimalizować czas pracy całej linii produkcyjnej (makespan).

2.5 Rozwiązanie problemu
3. Jak działa brute force

Brute Force – czyli szukanie optymalnego rozwiązania przez sprawdzenie wszystkich permutacji
Brute Force jest idealny do porównań i testów — np. możemy sprawdzić, czy algorytmy heurystyczne (jak Johnson) dają rozwiązanie optymalne.
W mojej aplikacji Brute Force używa dokładnie tego podejścia: generuje wszystkie kolejności i wybiera najlepszą.

Brute Force:

    Generuje wszystkie możliwe kolejności zadań.

    Dla każdej kolejności oblicza czas całkowitego wykonania (makespan).

    Wybiera kolejność z najmniejszym makespanem.

📌 Zaleta: znajduje rozwiązanie optymalne.
📌 Wada: działa wolno przy większej liczbie zadań (silnia – n!).

1. A → B → C
2. A → C → B
3. B → A → C
4. B → C → A
5. C → A → B
6. C → B → A

| Kolejność | Makespan |
| --------- | -------- |
| A B C     | 20       |
| A C B     | 18 ✅     |
| B A C     | 22       |
| B C A     | 19       |
| C A B     | 21       |
| C B A     | 25       |

Najlepsza kolejność (ACB)

Złożoność: O(n! x n x m)
n - liczba zadań
m - liczba maszyn



4. Algorytmy jakie są + matma
5. Implementacja algorytmów
6. Wykresy - porównanie wyników - różne problemy (demo)
7. Wykresy - porównanie czasu wykonywania obliczeń (demo)
8. Interactive demo



### Czym jest szeregowanie zadań?

Szeregowanie zadań (ang. *Job Scheduling*) to proces ustalania kolejności wykonywania zadań (np. prac budowlanych, zadań produkcyjnych czy operacji na maszynach), tak aby **zoptymalizować** pewien cel – najczęściej **czas zakończenia wszystkich zadań (tzw. makespan)**.

W praktyce chodzi o to, aby wykonać dane prace w możliwie najkrótszym czasie przy zachowaniu ograniczeń np. kolejności operacji, dostępności maszyn czy zasobów.

---

### 🏗️ **Przykład z prezentacji**

Prezentacja opiera się na przykładzie firmy budowlanej, która:

* musi wyremontować 4 mieszkania,
* zatrudnia 3 brygady (np. elektrycy, tynkarze, glazurnicy),
* każda brygada wykonuje swoje zadania w określonej kolejności i czasie.

Zadaniem jest ustalić **kolejność mieszkań**, aby całość remontu trwała **jak najkrócej**. Nie zmienia się kolejności prac (np. najpierw elektryka, potem tynk, potem glazura), ale **kolejność mieszkań**, w których te prace się odbywają.

---

### 🧮 **Na czym polega optymalizacja?**

Zmiana kolejności realizacji mieszkań może znacząco wpłynąć na łączny czas realizacji:

* Kolejność `1 → 2 → 3 → 4` = 24 dni
* Kolejność `3 → 2 → 4 → 1` = 23 dni
* Kolejność `2 → 4 → 1 → 3` = **17 dni** (optymalna)

Twoja aplikacja robi dokładnie to samo – pozwala użytkownikowi wprowadzić dane (czasy operacji) i dobrać **algorytm szeregowania**, który oblicza:

✅ Optymalną kolejność zadań (np. mieszkań lub zamówień)
✅ Łączny czas potrzebny na ich realizację
✅ Harmonogram zadań w formie wykresu Gantta

---

### 🛠️ **Algorytmy w Twojej aplikacji**

* **Algorytm Johnsona** – działa dla **2 maszyn** (lub brygad). Szybki i efektywny, wykorzystuje specjalną regułę porównywania czasów wykonania.

* **Algorytm Łomnickiego i Brown-Łomnickiego** – dla **3 maszyn**. Przeszukują przestrzeń możliwych permutacji, stosując podejście dokładne lub z ograniczaniem.

* **Brute Force** – sprawdza **wszystkie możliwe kolejności**. Bardzo dokładny, ale wolny przy dużej liczbie zadań.

---

### 📊 Jak to pokazać?

W prezentacji możesz:

1. Pokazać przykładową tabelę z czasami (tak jak w PDF).
2. Porównać różne kolejności i ich wpływ na czas końcowy.
3. Zaprezentować wykres Gantta generowany przez aplikację.
4. Podsumować: **im lepszy algorytm, tym krótszy czas – tym większa oszczędność.**
