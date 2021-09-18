import random
import re
import os


def main():
    # os.system("cls")
    open_tiles = 0
    alive = True

    try:
        m, n = map(int, input("[?] Введите размеры поля (через пробел): ").split())
    except ValueError:
        raise ValueError("[!] Вы ввели неверные размеры поля!")
    if m * n <= 1 or m < 0 or n < 0:
        raise Exception("[!] Поле должно иметь больше одной клетки!")

    try:
        mine_count = int(input("[?] Введите количество мин: "))
    except ValueError:
        raise ValueError("[!] Вы ввели неверное количество мин!")
    if mine_count <= 0 or mine_count >= m * n:
        raise Exception("[!] Мин должно быть больше нуля и меньше, чем клеток на поле!")

    player_field = [[0 for i in range(m)] for j in range(n)]
    answer_field = [[0 for i in range(m)] for j in range(n)]

    for _ in range(mine_count):
        i = random.randint(0, m - 1)
        j = random.randint(0, n - 1)

        if answer_field[i][j] == 0:
            answer_field[i][j] = 1
        else:
            _ -= 1

    while open_tiles < m * n - mine_count and alive:
        # os.system("cls")
        user_cmd = [0, 0, "Action"]
        print(player_field)  # TODO: заменить show_field()
        print("[?] Введите ваше следующее действие в формате [X, Y, Flag/Open]: ")
        user_input = input()  # TODO: снизу полный пиздец
        if re.match(r"\[[0-9]+, [0-9]+, (Flag|Open)\]", user_input) \
                and 0 <= int(re.findall(r"[0-9]+", user_input)[0]) < m \
                and 0 <= int(re.findall(r"[0-9]+", user_input)[1]) < n:
            user_cmd = [int(re.findall(r"[0-9]+", user_input)[0]), int(re.findall(r"[0-9]+", user_input)[1]), user_input[-5:-1]]
        else:
            print("[!] Вы ввели неправильную команду!")


if __name__ == "__main__":
    main()
