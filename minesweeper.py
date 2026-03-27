import random
import re
import os
from time import sleep
from collections import deque

def main():
    encode_key = 'tinkovf-edu_zxc1'  # ключ для шифрования сохранения
    dictionary = '0123456789abcdef'

    # получить координаты всех соседних клеток
    def get_neighbors(i, j, n, m):
        answer = []
        for di in range(i-1, i+2):
            for dj in range(j-1, j+2):
                if 0 <= di < n and 0 <= dj < m and (di != i or dj != j):
                    answer.append((di, dj))
        return answer

    # раскрыть содержимое клетки (итеративный BFS)
    def open_tile(i, j, answer_field, player_field, alive):
        # если клетка уже открыта или помечена флагом – не открываем
        if answer_field[i][j] in (2, 3, 4):
            return answer_field, player_field, alive

        # если наступили на мину
        if answer_field[i][j] == 1:
            alive = False
            return answer_field, player_field, alive

        # BFS для раскрытия области
        queue = deque()
        queue.append((i, j))
        visited = set()
        visited.add((i, j))

        while queue:
            x, y = queue.popleft()
            if answer_field[x][y] in (2, 3, 4):
                continue

            mines_near = get_nearby_mines(n, m, x, y, answer_field)
            if mines_near > 0:
                player_field[x][y] = str(mines_near)
                answer_field[x][y] = 2
            else:
                player_field[x][y] = "-"
                answer_field[x][y] = 2
                # добавляем всех соседей, которые ещё не обработаны
                for nx, ny in get_neighbors(x, y, n, m):
                    if (nx, ny) not in visited and answer_field[nx][ny] not in (2, 3, 4):
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        return answer_field, player_field, alive

    def clear():  # очистить экран
        os.system("cls" if os.name == 'nt' else "clear")

    def load_game():  # загрузка сэйва
        try:
            with open("sa.ve", "r") as f:
                content = f.readlines()
        except FileNotFoundError:
            return None

        if len(content) < 2:
            return None

        # получение размерности поля из сэйва
        size_line = content[0].strip()
        if '*' not in size_line:
            return None
        m, n = map(int, size_line.split('*'))

        # расшифровка матрицы ответов
        answers_line = content[1].strip()
        answers = ""
        for symbol in answers_line:
            try:
                answers += dictionary[encode_key.index(symbol)]
            except ValueError:
                return None
        try:
            answers = str(int(answers, 16))
        except ValueError:
            return None

        # вычитаем прибавленные при сохранении единицы
        temp = ""
        for symbol in answers:
            temp += str(int(symbol) - 1)
        answers = temp

        if len(answers) != n * m:
            return None

        open_tiles = answers.count("2")
        mine_count = answers.count("1")

        answer_field = [[0 for _ in range(m)] for _ in range(n)]
        player_field = [[0 for _ in range(m)] for _ in range(n)]

        # заполнение поля ответов
        cntr = 0
        for i in range(n):
            for j in range(m):
                answer_field[i][j] = int(answers[cntr])
                cntr += 1

        # основываясь на ответах, заполняет поле игрока
        for i in range(n):
            for j in range(m):
                if answer_field[i][j] in (0, 1):
                    player_field[i][j] = 0
                elif answer_field[i][j] in (3, 4):
                    player_field[i][j] = "x"
                elif answer_field[i][j] == 2:
                    mines = get_nearby_mines(n, m, i, j, answer_field)
                    player_field[i][j] = "-" if mines == 0 else str(mines)

        print("[$] Игра успешно загружена!")
        return m, n, mine_count, open_tiles, answer_field, player_field

    # очистить сэйв (после проигрыша или победы)
    def clear_save():
        try:
            os.remove("sa.ve")
        except FileNotFoundError:
            pass

    def save_game():
        with open("sa.ve", "w") as f:
            answers_encoded = ""
            answers = ""

            # записываем значения клеток в строку
            for i in range(n):
                for j in range(m):
                    answers += str(answer_field[i][j] + 1)  # +1 во избежание проблемы с нулями в начале матрицы

            # переводим ответы в 16сс и шифруем согласно ключу
            answers = hex(int(answers))[2:]
            for symbol in answers:
                answers_encoded += encode_key[dictionary.index(symbol)]

            # сохранение размеров матрицы и зашифрованных ответов
            f.write(f"{m}*{n}\n{answers_encoded}\n")

    # получить количество мин по-соседству
    def get_nearby_mines(n, m, i, j, answer_field):
        mines = 0
        for ni, nj in get_neighbors(i, j, n, m):
            if answer_field[ni][nj] in (1, 3):
                mines += 1
        return mines

    # отобразить игровое поле
    def show_field():
        for i in range(n):
            row = ""
            for j in range(m):
                row += f"[{player_field[i][j]}]"
            print(row)

    # -------------------- основная логика игры --------------------
    while True:
        clear()

        open_tiles = 0
        alive = True

        # попытка загрузить сохранение
        loaded = load_game()
        if loaded is None:
            alive = True

            # ввод размерностей поля
            try:
                n, m = map(int, input("[?] Введите размеры поля (через пробел): ").split())
            except ValueError:
                raise ValueError("[!] Вы ввели неверные размеры поля!")
            if m * n <= 1 or m < 0 or n < 0:
                raise Exception("[!] Поле должно иметь больше одной клетки!")

            # ввод количества мин
            try:
                mine_count = int(input("[?] Введите количество мин: "))
            except ValueError:
                raise ValueError("[!] Вы ввели неверное количество мин!")
            if mine_count <= 0 or mine_count >= m * n:
                raise Exception("[!] Мин должно быть больше нуля и меньше, чем клеток на поле!")

            player_field = [[0 for _ in range(m)] for _ in range(n)]
            answer_field = [[0 for _ in range(m)] for _ in range(n)]

            # генерация мин
            for _ in range(mine_count):
                i = random.randint(0, m - 1)
                j = random.randint(0, n - 1)
                if answer_field[j][i] == 0:
                    answer_field[j][i] = 1
                else:
                    _ -= 1
            save_game()
        else:
            m, n, mine_count, open_tiles, answer_field, player_field = loaded

        # цикл игры
        while open_tiles < m * n - mine_count and alive:
            show_field()
            print("[?] Введите ваше следующее действие в формате [X, Y, Flag/Open]: ")
            user_input = input()

            # проверка пользовательского ввода (пробелы не обязательны)
            match = re.match(r"\[(\d+),\s*(\d+),\s*(Flag|Open)\]", user_input)
            if match:
                x, y, action = match.groups()
                x, y = int(x), int(y)
                if 0 <= x < m and 0 <= y < n:
                    # преобразуем координаты (игрок видит сверху вниз, а матрица хранит снизу вверх)
                    row = n - 1 - y
                    col = x

                    if action == "Flag":
                        if player_field[row][col] != "x":
                            player_field[row][col] = "x"
                            answer_field[row][col] = 3 if answer_field[row][col] == 1 else 4
                        else:
                            player_field[row][col] = 0
                            answer_field[row][col] = 1 if answer_field[row][col] == 3 else 0
                        clear()
                        save_game()
                    else:  # Open
                        answer_field, player_field, alive = open_tile(row, col, answer_field, player_field, alive)
                        clear()
                        save_game()
                else:
                    clear()
                    print("[!] Координаты выходят за пределы поля!")
            else:
                clear()
                print("[!] Вы ввели неправильную команду!")

            # подсчёт открытых клеток
            open_tiles = sum(1 for i in range(n) for j in range(m) if answer_field[i][j] == 2)

        if alive:
            clear()
            print("[$] Вы победили!")
        else:
            clear()
            print("[!] К сожалению, Вы взорвались..")

        print("[?] Следующая игра начнётся через 10 секунд..")
        sleep(10)
        clear_save()
        # цикл продолжится автоматически

if __name__ == "__main__":
    main()