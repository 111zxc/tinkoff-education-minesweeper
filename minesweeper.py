import random


def main():
    try:
        m, n = map(int, input("[?] Введите размеры поля (через пробел): ").split())
    except ValueError:
        raise ValueError("[!] Вы ввели неверные размеры поля!")
    if m*n <= 1 or m < 0 or n < 0:
        raise Exception("[!] Поле должно иметь больше одной клетки!")

    try:
        mine_count = int(input("[?] Введите количество мин: "))
    except ValueError:
        raise ValueError("[!] Вы ввели неверное количество мин!")
    if mine_count <= 0 or mine_count >= m * n:
        raise Exception("[!] Мин должно быть больше нуля и меньше, чем клеток на поле!")

    player_field = [[0 for i in range(n)] for j in range(m)]
    answer_field = [[0 for i in range(n)] for j in range(m)]

    for _ in range(mine_count):
        i = random.randint(0, m-1)
        j = random.randint(0, n-1)

        if answer_field[i][j] == 0:
            answer_field[i][j] = 1
        else:
            _ -= 1


if __name__ == "__main__":
    main()
