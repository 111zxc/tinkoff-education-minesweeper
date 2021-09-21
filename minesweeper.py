import random
import re
import os

 

def main():
    encode_key = 'tinkovf-edu_zxc1'
    dictionary = '0123456789abcdef'

    def clear():
        os.system("cls" if os.name == 'nt' else "clear")

    def clear_save():
        file = open("sa.ve", "w")
        file.close()

    def save_game():  # TODO: закрывать ли ваще файл?
        file = open("sa.ve", "w")  # файл сохранения
        
        answers_encoded = ""
        answers = ""
        
        # записываем значения клеток в строку
        for i in range(n):
            for j in range(m):
                answers += str(answer_field[i][j])
        
        # переводим ответы в 16сс и шифруем согласно ключу
        answers = hex(int(answers))[2:]
        for symbol in answers:
            answers_encoded += encode_key[dictionary.index(symbol)]
        
        # сохранение размеров матрицы и зашифрованных ответов
        file.write(f"{m}*{n},{answers_encoded}")
        file.close()  # заканчиваем работу с файлом сохранения

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

    clear()  # TODO: на линухе clear
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
    save_game()

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
            user_cmd = [n - 1 - int(re.findall(r"[0-9]+", user_input)[1]), int(re.findall(r"[0-9]+", user_input)[0]),
                        user_input[-5:-1]]

            if user_cmd[2] == 'Flag':  # если Action = Flag
                if player_field[user_cmd[0]][user_cmd[1]] != "x":  # если клетка еще не открыта и не помечена флагом
                    player_field[user_cmd[0]][user_cmd[1]] = "x"  # помечаем клетку флагом
                    clear()
                    save_game()
                else:
                    player_field[user_cmd[0]][user_cmd[1]] = 0  # если клетка уже помечена флагом, снимаем флаг
                    clear()
                    save_game()
            elif user_cmd[2] == 'Open':  # если Action = Open
                if answer_field[user_cmd[0]][user_cmd[1]] != 2:  # можем открыть клетку, только если она еще не открыта
                    if answer_field[user_cmd[0]][user_cmd[1]] == 1:  # взрываемся, если открыли мину
                        clear()
                        print("[!] К сожалению, вы взорвались.")
                        alive = False
                        clear_save()
                    else:  # если открыли не мину
                        if get_nearby_mines(user_cmd[0], user_cmd[1]) > 0:
                            player_field[user_cmd[0]][user_cmd[1]] = str(get_nearby_mines(user_cmd[0], user_cmd[1]))
                            clear()
                            save_game()
                            # возвращаем количество мин рядом цифрой только если их больше 0 (иначе 0 - неоткрытая
                            # клетка, конфликт)
                        else:
                            clear()
                            player_field[user_cmd[0]][user_cmd[1]] = "-"  # возвращаем дэш, если рядом 0 мин
                        open_tiles += 1  # отслеживаем количество открытых клеток, чтобы не дать поиграть в
                        answer_field[user_cmd[0]][user_cmd[1]] = 2 # завершенную игру
                        save_game()
                elif player_field[user_cmd[0]][user_cmd[1]] == "x":
                    # не даём открывать клетки, помеченные флагом. Надеюсь, так надо.
                    clear()
                    print("[?] На эту клетку вы поставили флаг. Снимите его, чтобы раскрыть содержимое этой клетки.")
                    save_game()
                else:
                    clear()
                    print("[?] Вы уже открывали эту клетку.")  # хэндл открытия уже открытой клетки
                    save_game()
        else:
            clear()
            print("[!] Вы ввели неправильную команду!")  # хэндл неправильного ввода

    if alive:  # винкондишн достигается, если цикл вайл закончен (нет неоткрытых клеток не мин) и мы остались в живых
        clear()
        print("[$] Вы победили!")
        clear_save()


if __name__ == "__main__":
    main()
