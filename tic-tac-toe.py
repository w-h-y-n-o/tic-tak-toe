import random


# функция для выбора режима игры
def menu():
    set_command = ['start', 'exit', 'easy', 'medium', 'hard', 'user']
    mode_status = []
    while True:
        mode = input('Input command: ')
        # mode = 'start easy easy'
        mode = mode.split()
        if set(mode).issubset(set_command):
            if len(mode) != 0:
                if mode[0] == 'start':
                    if len(mode) == 3:
                        for player in mode[1:]:
                            if (player == 'easy') or (player == 'medium') or (player == 'user') or (player == 'hard'):
                                mode_status.append(player)
                            else:
                                print('Bad parameters!')
                                continue
                        mode_status = ' vs '.join(mode_status)
                        return mode_status
                    else:
                        print('Bad parameters!')
                        continue
                elif (mode[0] == 'exit') and (len(mode) == 1):
                    mode_status = 'exit'
                    return mode_status
                else:
                    print('Bad parameters!')
                    continue
            else:
                print('Bad parameters!')
                continue
        else:
            print('Bad parameters!')
            continue


# функция для формирования пустого поля
def initial_field_state():
    test_field = ['___', '___', '___']
    field = []
    for line in test_field:
        row = []
        for cell in line:
            if cell == 'X':
                row.append(cell)
            elif cell == 'O':
                row.append(cell)
            elif cell == '_':
                row.append(' ')
        field.append(row)

    print('---------')
    print('|', *field[0], '|')
    print('|', *field[1], '|')
    print('|', *field[2], '|')
    print('---------')
    return field


# функция для нахождения конечного состояния поля
def status_field(board):
    status = 0
    # проверка конечных состояний в строках
    for row in board:
        if all([i == 'X' for i in row]):
            status = 'X wins'
            return status
        elif all([i == 'O' for i in row]):
            status = 'O wins'
            return status
        elif any([i == ' ' for i in row]):
            status = None
    # проверка конечных состояний в столбцах
    for i in range(3):
        column = [board[0][i], board[1][i], board[2][i]]
        if all([n == 'X' for n in column]):
            status = 'X wins'
            return status
        elif all([n == 'O' for n in column]):
            status = 'O wins'
            return status
        i += 1
    # проверка конечных состояний в диагоналях
    for j in range(2):
        if j == 1:
            diag = [board[0][j + 1], board[1][j], board[2][j - 1]]
        else:
            diag = [board[0][j], board[1][j + 1], board[2][j + 2]]
        if all([n == 'X' for n in diag]):
            status = 'X wins'
            return status
        elif all([n == 'O' for n in diag]):
            status = 'O wins'
            return status
        j += 1

    if status is None:
        return status
    else:
        status = 'Draw'
    return status


def count_score(status_new, turn_ai):
    score = None
    if turn_ai == 1:
        if status_new == 'X wins':
            score = 10
        elif status_new == 'O wins':
            score = -10
        elif status_new == 'Draw':
            score = 0
    else:
        if status_new == 'X wins':
            score = -10
        elif status_new == 'O wins':
            score = 10
        elif status_new == 'Draw':
            score = 0
    return score


def minimax(board, empty_cell, turn_ai):  # turn_ai: 1 - ход машины, 0 - ход игрока
    score = None
    empty = []
    i = 0
    j = 0
    x = 0
    o = 0
    new_field = board

    for row in new_field:
        x += row.count('X')
        o += row.count('O')

    if x <= o:
        step = 'X'
    else:
        step = 'O'

    new_field[empty_cell[0]][empty_cell[1]] = step
    status_new = status_field(new_field)
    if status_new is not None:
        score = count_score(status_new, turn_ai)
        return score
    else:
        if turn_ai == 1:
            turn_ai = 0
        else:
            turn_ai = 1
        for row in new_field:
            for cell in row:
                if cell == ' ':
                    empty.append([i, j])
                j += 1
            j = 0
            i += 1
        for empty_cell in empty:
            new_field[empty_cell[0]][empty_cell[1]] = step
            score = minimax(new_field, empty_cell, turn_ai)
        return score


# функция, которая поочерёдно делает шаги
def turn(mode, board):
    coordinates = []
    empty_cell = 0
    n = 0
    x = 0
    o = 0
    for row in board:
        x += row.count('X')
        o += row.count('O')

    if mode == 'user vs user':
        while True:
            step = input('Enter the coordinates: ').replace(' ', '')
            try:
                coordinates = [int(i) for i in step]
            except ValueError:
                print('You should enter numbers!')
                continue

            if len(coordinates) == 0:
                return board

            if any([((i > 3) or (i < 1)) for i in coordinates]):
                print('Coordinates should be from 1 to 3!')
                continue

            if board[coordinates[0] - 1][coordinates[1] - 1] != ' ':
                print('This cell is occupied! Choose another one!')
                continue
            break

        if x <= o:
            board[coordinates[0] - 1][coordinates[1] - 1] = 'X'
        else:
            board[coordinates[0] - 1][coordinates[1] - 1] = 'O'
    elif mode == 'easy vs easy':
        print('Making move level "easy"')
        while True:
            coordinates = [random.randint(1, 3), random.randint(1, 3)]
            if board[coordinates[0] - 1][coordinates[1] - 1] != ' ':
                continue
            break

        if x <= o:
            board[coordinates[0] - 1][coordinates[1] - 1] = 'X'
        else:
            board[coordinates[0] - 1][coordinates[1] - 1] = 'O'
    elif mode == 'medium vs medium':
        print('Making move level "medium"')
        while True:
            coordinates = [random.randint(1, 3), random.randint(1, 3)]
            if board[coordinates[0] - 1][coordinates[1] - 1] != ' ':
                continue
            break

        if x <= o:
            step = 'X'
        else:
            step = 'O'

        for row in board:
            if ((row.count('X') == 2) or (row.count('O') == 2)) and (row.count(' ') == 1):
                empty_cell = str(n) + str((''.join(row)).find(' '))
            n += 1

        for i in range(3):
            column = [board[0][i], board[1][i], board[2][i]]
            if ((column.count('X') == 2) or (column.count('O') == 2)) and (column.count(' ') == 1):
                empty_cell = str((''.join(column)).find(' ')) + str(i)
            i += 1

        diag1 = [board[0][2], board[1][1], board[2][0]]
        diag2 = [board[0][0], board[1][1], board[2][2]]
        if ((diag1.count('X') == 2) or (diag1.count('O') == 2)) and (diag1.count(' ') == 1):
            if str((''.join(diag1)).find(' ')) == 0:
                empty_cell = str((''.join(diag1)).find(' ')) + str(2)
            if str((''.join(diag1)).find(' ')) == 1:
                empty_cell = str((''.join(diag1)).find(' ')) + str(1)
            if str((''.join(diag1)).find(' ')) == 2:
                empty_cell = str((''.join(diag1)).find(' ')) + str(0)
        if ((diag2.count('X') == 2) or (diag2.count('O') == 2)) and (diag2.count(' ') == 1):
            if str((''.join(diag2)).find(' ')) == 0:
                empty_cell = str((''.join(diag2)).find(' ')) + str(0)
            if str((''.join(diag2)).find(' ')) == 1:
                empty_cell = str((''.join(diag2)).find(' ')) + str(1)
            if str((''.join(diag2)).find(' ')) == 2:
                empty_cell = str((''.join(diag2)).find(' ')) + str(2)

        if empty_cell == 0:
            board[coordinates[0] - 1][coordinates[1] - 1] = step
        else:
            board[int(empty_cell[0])][int(empty_cell[1])] = step
    elif mode == 'hard vs hard':
        print('Making move level "hard"')
        empty = []
        i = 0
        j = 0
        turn_ai = 1
        all_score = []

        if x <= o:
            step = 'X'
        else:
            step = 'O'

        for row in board:
            for cell in row:
                if cell == ' ':
                    empty.append([i, j])
                j += 1
            j = 0
            i += 1

        for empty_cell in empty:
            score = minimax(board, empty_cell, turn_ai)
            all_score.append(score)

        coordinates = empty[(all_score.index(max(all_score)))]

        board[coordinates[0]][coordinates[1]] = step

    print('---------')
    print('|', *board[0], '|')
    print('|', *board[1], '|')
    print('|', *board[2], '|')
    print('---------')
    return board


mode = menu()
field = initial_field_state()
status = status_field(field)
while mode != 'exit':
    while status is None:
        if (mode == 'user vs user') or (mode == 'easy vs easy'):
            field = turn(mode, field)
        elif mode == 'user vs easy':
            field = turn('user vs user', field)
            mode = 'easy vs user'
        elif mode == 'easy vs user':
            field = turn('easy vs easy', field)
            mode = 'user vs easy'
        elif mode == 'medium vs medium':
            field = turn(mode, field)
        elif mode == 'user vs medium':
            field = turn('user vs user', field)
            mode = 'medium vs user'
        elif mode == 'medium vs user':
            field = turn('medium vs medium', field)
            mode = 'user vs medium'
        elif mode == 'hard vs hard':
            field = turn(mode, field)
        elif mode == 'user vs hard':
            field = turn('user vs user', field)
            mode = 'hard vs user'
        elif mode == 'hard vs user':
            field = turn('hard vs hard', field)
            mode = 'user vs hard'
        status = status_field(field)
    print(status)
    mode = menu()
    field = initial_field_state()
    status = status_field(field)
