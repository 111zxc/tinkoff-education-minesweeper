import random
import re
import os


def main():
    # получить количество мин по-соседству с данной клеткой; используется после открытия клетки
    def get_nearby_mines(i, j):  # TODO: это как-то можно лучше сделать?
        if i == 0 and j == 0:  # верхний левый угол
            mines = answer_field[0][1] + answer_field[1][0] + answer_field[1][1]
        elif i == n - 1 and j == 0:  # нижний левый угол
            mines = answer_field[n - 1][1] + answer_field[n - 2][0] + answer_field[n - 2][1]
        elif i == 0 and j == m - 1:  # угол)
            mines = answer_field[i][j - 1] + answer_field[i + 1][j] + answer_field[i + 1][j - 1]
        elif i == n - 1 and j == m - 1:  # corner))))))))
            mines = answer_field[i][j - 1] + answer_field[i - 1][j - 1] + answer_field[i - 1][j]
        elif i == 0:  # боковая стенка1
            mines = answer_field[i][j + 1] + answer_field[i][j - 1] + answer_field[i + 1][j] + answer_field[i + 1][
                j - 1] + answer_field[i + 1][j + 1]
        elif i == n - 1:  # боковая стенка2
            mines = answer_field[i][j + 1] + answer_field[i][j - 1] + answer_field[i - 1][j] + answer_field[i - 1][
                j - 1] + answer_field[i - 1][j + 1]
        elif j == 0:  # боковая стенка3
            mines = answer_field[i + 1][j] + answer_field[i - 1][j] + answer_field[i][j + 1] + answer_field[i + 1][
                j + 1] + answer_field[i - 1][j + 1]
        elif j == m - 1:  # боковая стенка4
            mines = answer_field[i + 1][j] + answer_field[i - 1][j] + answer_field[i][j - 1] + answer_field[i + 1][
                j - 1] + answer_field[i - 1][j - 1]
        else:  # клетки посередине
            mines = answer_field[i][j + 1] + answer_field[i][j - 1] + answer_field[i + 1][j] + answer_field[i + 1][
                j + 1] + answer_field[i + 1][j - 1] + \
                    answer_field[i - 1][j] + answer_field[i - 1][j + 1] + answer_field[i - 1][j - 1]
        return mines

    # отобразить игровое поле в читабельном виде
    def show_field():
        for i in range(n):
            row = ""
            for j in range(m):
                row += f"[{player_field[i][j]}]"
            print(row)

    os.system("cls")  # TODO: на линухе clear
    open_tiles = 0  # количество открытых клеток для учета состояния игры
    alive = True  # игра идет пока есть пустые клетки и вы живы

    # ввод размерностей поля (не намудрил ли я с координатами?)
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
    answer_field = [[0 for i in range(m)] for j in range(n)]  # матрица поля с ответами TODO: сохранять вот это

    # генерация мин
    for _ in range(mine_count):
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)

        if answer_field[j][i] == 0:
            answer_field[j][i] = 1
        else:
            _ -= 1

    # цикл игры, работает, пока мы живы и существуют неоткрытые клетки, не являющиеся минами
    while open_tiles < m * n - mine_count and alive:
        user_cmd = [0, 0, "Action"]  # [X, Y, (Flag|Open)]
        show_field()

        print("[?] Введите ваше следующее действие в формате [X, Y, Flag/Open]: ")
        user_input = input()

        # проверка пользовательского ввода TODO: это выглядит ужасно
        if re.match(r"\[[0-9]+, [0-9]+, (Flag|Open)\]", user_input) \
                and 0 <= int(re.findall(r"[0-9]+", user_input)[1]) < n \
                and 0 <= int(re.findall(r"[0-9]+", user_input)[0]) < m:
            user_cmd = [n-1 - int(re.findall(r"[0-9]+", user_input)[1]), int(re.findall(r"[0-9]+", user_input)[0]),
                        user_input[-5:-1]]

            if user_cmd[2] == 'Flag':  # если Action = Flag
                if player_field[user_cmd[0]][user_cmd[1]] != "x":  # если клетка еще не открыта и не помечена флагом
                    player_field[user_cmd[0]][user_cmd[1]] = "x"   # помечаем клетку флагом
                    os.system("cls")
                else:
                    player_field[user_cmd[0]][user_cmd[1]] = 0  # если клетка уже помечена флагом, снимаем флаг
                    os.system("cls")
            elif user_cmd[2] == 'Open':  # если Action = Open
                if player_field[user_cmd[0]][user_cmd[1]] == 0:  # можем открыть клетку, только если она еще не открыта
                    if answer_field[user_cmd[0]][user_cmd[1]] == 1:  # взрываемся, если открыли мину
                        os.system("cls")
                        print("[!] К сожалению, вы взорвались.")
                        alive = False
                    else:  # если открыли не мину
                        if get_nearby_mines(user_cmd[0], user_cmd[1]) > 0:
                            player_field[user_cmd[0]][user_cmd[1]] = str(get_nearby_mines(user_cmd[0], user_cmd[1]))
                            os.system("cls")
                            # возвращаем количество мин рядом цифрой только если их больше 0 (иначе 0 - неоткрытая
                            # клетка, конфликт)
                        else:
                            os.system("cls")
                            player_field[user_cmd[0]][user_cmd[1]] = "-"  # возвращаем дэш, если рядом 0 мин
                        open_tiles += 1  # отслеживаем количество открытых клеток, чтобы не дать поиграть в
                        # завершенную игру
                elif player_field[user_cmd[0]][user_cmd[1]] == "x":
                    # не даём открывать клетки, помеченные флагом. Надеюсь, так надо.
                    os.system("cls")
                    print("[?] На эту клетку вы поставили флаг. Снимите его, чтобы раскрыть содержимое этой клетки.")
                else:
                    os.system("cls")
                    print("[?] Вы уже открывали эту клетку.")  # хэндл открытия уже открытой клетки
        else:
            os.system("cls")
            print("[!] Вы ввели неправильную команду!")  # хэндл неправильного ввода

    if alive:  # винкондишн достигается, если цикл вайл закончен (нет неоткрытых клеток не мин) и мы остались в живых
        os.system("cls")
        print("[$] Вы победили!")


if __name__ == "__main__":
    main()
