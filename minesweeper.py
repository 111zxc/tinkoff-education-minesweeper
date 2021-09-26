import random
import os
from time import sleep

def main():
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
                        open_tile(element[0], element[1], answer_field, player_field, alive, limit_counter)
        elif player_field[i][j] == "x":
            # не даём открывать клетки, помеченные флагом. Надеюсь, так надо
            print("[?] На эту клетку вы поставили флаг. Снимите его, чтобы раскрыть содержимое этой клетки.")
        else:
            print("[?] Вы уже открывали эту клетку.")  # хэндл открытия уже открытой клетки       
        return answer_field, player_field, alive

    def clear():  # очистить экран
        os.system("cls" if os.name == 'nt' else "clear")

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

    # цикл игры; работает, пока мы живы и существуют неоткрытые клетки, не являющиеся минами
    while open_tiles < m * n - mine_count and alive:
        show_field()

        # действие алгоритма
        value_map = [[0 for i in range(m)] for j in range(n)]
        tempCounter = 0
        for i in player_field:
            for j in i:
                if j == 0:
                    tempCounter += 1

        if tempCounter == m*n:
            # хитмап для первого хода
            for i in range(n):
                for j in range(m):
                    nearby_tiles = len(get_all_near_tiles(i, j, n, m))
                    value_map[i][j] = 1 - (mine_count/(n*m)) + nearby_tiles
        else:  # хитмап для последующих ходов
            for i in range(n):
                for j in range(m):
                    if player_field[i][j] != 0:  # если клетка уже открыта, мы не будем ее открывать
                        value_map[i][j] = -99
                    else:
                        value_map[i][j] = 1
                        
                        closed_tiles_nearby = 0
                        for el in get_all_near_tiles(i, j, n, m):
                            if player_field[el[0]][el[1]] == 0:
                                closed_tiles_nearby += 1
                        value_map[i][j] += closed_tiles_nearby/(m*n-open_tiles)

                        for el in get_all_near_tiles(i, j, n, m):
                            if player_field[el[0]][el[1]] != 0 and player_field[el[0]][el[1]] != '-':
                                x = int(player_field[el[0]][el[1]])
                                num_closed_tiles = 0
                                for el2 in get_all_near_tiles(el[0], el[1], n, m):
                                    if player_field[el2[0]][el2[1]] == 0:
                                        num_closed_tiles += 1
                                value_map[i][j] -= x/num_closed_tiles
        # выбор самой выгодной клетки (max)
        maxel = -1000
        el_i, el_j = 0, 0
        for i in range(n):
            for j in range(m):
                if value_map[i][j] > maxel and value_map != -99:
                    maxel = value_map[i][j]
                    el_i = i
                    el_j = j
        print(f"[?] Алгоритм решил выбрать клетку с координатами ({el_i}, {el_j})!")
        open_tile(el_i, el_j, answer_field, player_field, alive)
        ## конец работы алгоритма ##
        
        open_tiles = 0
        for i in range(n):
            for j in range(m):
                if answer_field[i][j] == 2: open_tiles += 1
                        

    if alive:  # винкондишн достигается, если цикл вайл закончен (нет неоткрытых клеток не мин) и мы остались в живых
        print("[$] Алгоритм победил!")
        show_field()
    else:
        print("[!] К сожалению, даже алгоритм проиграл..")
    print("[?] Следующая игра начнётся через 100 секунд..")
    sleep(100)
    main()


if __name__ == "__main__":
    main()
