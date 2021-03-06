import random
import re
import os
from time import sleep

def main():
    encode_key = 'tinkovf-edu_zxc1'  # ключ для шифрования сохранения
    dictionary = '0123456789abcdef'

    # получить координаты всех соседних клеток
    def get_all_near_tiles(i, j, n, m):
        answer = []
        for _ in range(i-1, i+2):
            for __ in range(j-1, j+2):
                if 0 <= __ < m and 0 <= _ < n and (_ != i or j != __):
                    answer.append((_, __))
        return answer

    def open_tile(i, j, answer_field, player_field, alive, limit_counter=0):  # раскрыть содержимое клетки
        limit_counter += 1
        if answer_field[i][j] != (2, 3, 4):  # можем открыть клетку, только если она еще не открыта и не флаг
            if limit_counter >= 4:  # лимит, чтобы не впадать в максимальную глубину рекурсии TODO: ваще это неправильно
                return answer_field, player_field, alive
            if answer_field[i][j] == 1:  # взрываемся, если открыли мину
                alive = False
            else:  # если открыли не мину
                if get_nearby_mines(n, m, i, j, answer_field) > 0:
                    player_field[i][j] = str(get_nearby_mines(n, m, i, j, answer_field))
                    answer_field[i][j] = 2
                    # возвращаем количество мин рядом цифрой только если их больше 0 (иначе 0 - неоткрытая
                    # клетка, конфликт)
                else:
                    player_field[i][j] = "-"  # возвращаем дэш, если рядом 0 мин
                    answer_field[i][j] = 2
                    for element in get_all_near_tiles(i, j, n, m):  # если рядом нет мин, открываем все клетки поблизости
                        answer_field, player_field, alive = open_tile(element[0], element[1], answer_field, player_field, alive, limit_counter)
                save_game()
                clear()
        elif player_field[i][j] == "x":
            # не даём открывать клетки, помеченные флагом. Надеюсь, так надо
            clear()
            print("[?] На эту клетку вы поставили флаг. Снимите его, чтобы раскрыть содержимое этой клетки.")
            save_game()
        else:
            clear()
            print("[?] Вы уже открывали эту клетку.")  # хэндл открытия уже открытой клетки
            save_game()        
        return answer_field, player_field, alive

    def clear():  # очистить экран
        os.system("cls" if os.name == 'nt' else "clear")

    def load_game():  # загрузка сэйва
        f = open("sa.ve")
        content = f.readlines()

        # получение размерности поля из сэйва
        size = content[0][:-1]
        m, n = int(size[0:size.index("*")]), int(size[size.index("*")+1:])

        # расшифровка матрицы ответов
        answers = ""
        for symbol in content[1]:
            answers += dictionary[encode_key.index(symbol)]
        answers = str(int(answers, 16))

        # вычитаем прибавленные при сохранении единицы
        temp = ""
        for symbol in answers:
            temp += str(int(symbol) - 1)
        answers = temp

        open_tiles = answers.count("2")
        mine_count = answers.count("1")
        
        answer_field = [[0 for i in range(m)] for j in range(n)]
        player_field = [[0 for i in range(m)] for j in range(n)]
        
        # заполнение поля ответов
        cntr = 0
        for i in range(n):
            for j in range(m):
                answer_field[i][j] = int(answers[cntr])
                cntr += 1

        # основываясь на ответах, заполняет поле игрока
        for i in range(n):
            for j in range(m):
                if answer_field[i][j] == (0 or 1):
                    player_field[i][j] = 0
                if answer_field[i][j] == 3:
                    player_field[i][j] = "x"
                if answer_field[i][j] == 4:
                    player_field[i][j] = "x"
                if answer_field[i][j] == 2:
                    player_field[i][j] = "-" if get_nearby_mines(n, m, i, j, answer_field) == 0 else get_nearby_mines(n, m, i,j, answer_field)
        f.close()

        alive = True

        print("[$] Игра успешно загружена!")
        return m, n, mine_count, open_tiles, answer_field, player_field

    # очистить сэйв (после проигрыша или победы)
    def clear_save():
        file = open("sa.ve", "w")
        file.close()

    def save_game():
        file = open("sa.ve", "w")
        
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
        file.write(f"{m}*{n}\n{answers_encoded}")
        file.close()

    # получить количество мин по-соседству с данной клеткой; используется после открытия клетки
    def get_nearby_mines(n, m, i, j, answer_field):
        near_tiles = get_all_near_tiles(i, j, n, m)
        mines = 0
        for el in near_tiles:
            if answer_field[el[0]][el[1]] == 1 or answer_field[el[0]][el[1]] == 3: mines += 1
        return mines

    # отобразить игровое поле в читабельном виде
    def show_field():
        for i in range(n):
            row = ""
            for j in range(m):
                row += f"[{player_field[i][j]}]"
            print(row)

    clear()

    open_tiles = 0 # количество открытых клеток для учета состояния игры
    alive = True

    f = open("sa.ve")
    save_info = f.read() 
    f.close()

    if save_info == "": # если сэйва нет
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

        player_field = [[0 for i in range(m)] for j in range(n)]  # матрица поля, отображаемого игроку
        answer_field = [[0 for i in range(m)] for j in range(n)]  # матрица поля с ответами

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
        m, n, mine_count, open_tiles, answer_field, player_field = load_game()

    # цикл игры; работает, пока мы живы и существуют неоткрытые клетки, не являющиеся минами
    while open_tiles < m * n - mine_count and alive:

        user_cmd = [0, 0, "Action"]  # [X, Y, (Flag|Open)]
        show_field()
        
        print("[?] Введите ваше следующее действие в формате [X, Y, Flag/Open]: ")
        user_input = input()

        # проверка пользовательского ввода
        if re.match(r"\[[0-9]+, [0-9]+, (Flag|Open)\]", user_input) \
                and 0 <= int(re.findall(r"[0-9]+", user_input)[1]) < n \
                and 0 <= int(re.findall(r"[0-9]+", user_input)[0]) < m:
            user_cmd = [n - 1 - int(re.findall(r"[0-9]+", user_input)[1]), int(re.findall(r"[0-9]+", user_input)[0]),
                        user_input[-5:-1]]

            if user_cmd[2] == 'Flag':  # если Action = Flag
                if player_field[user_cmd[0]][user_cmd[1]] != "x":  # если клетка еще не открыта и не помечена флагом
                    player_field[user_cmd[0]][user_cmd[1]] = "x"  # помечаем клетку флагом
                    if answer_field[user_cmd[0]][user_cmd[1]] == 1:
                        answer_field[user_cmd[0]][user_cmd[1]] = 3
                    else:
                        answer_field[user_cmd[0]][user_cmd[1]] = 4
                    clear()
                    save_game()
                else:
                    player_field[user_cmd[0]][user_cmd[1]] = 0  # если клетка уже помечена флагом, снимаем флаг
                    if answer_field[user_cmd[0]][user_cmd[1]] == 3:
                        player_field[user_cmd[0]][user_cmd[1]] = 1
                    else:
                        player_field[user_cmd[0]][user_cmd[1]] = 0
                    clear()
                    save_game()
            elif user_cmd[2] == 'Open':  # если Action = Open
                answer_field, player_field, alive = open_tile(user_cmd[0], user_cmd[1], answer_field, player_field, alive)
        else:
            clear()
            print("[!] Вы ввели неправильную команду!")  # хэндл неправильного ввода
        open_tiles = 0
        for i in range(n):
            for j in range(m):
                if answer_field[i][j] == 2:
                    open_tiles += 1

    if alive:  # винкондишн достигается, если цикл вайл закончен (нет неоткрытых клеток не мин) и мы остались в живых
        clear()
        print("[$] Вы победили!")
    else:
        print("[!] К сожалению, Вы взорвались..")
    print("[?] Следующая игра начнётся через 10 секунд..    ")
    clear_save()
    sleep(10)
    main()


if __name__ == "__main__":
    main()
