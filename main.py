from tabulate import tabulate
from random import randint
from string import ascii_uppercase
from sys import argv
from os import system
from colorama import init, Fore
init()

class Game:
    __board: list = []
    __size: int = 9
    __cells: dict = {}
    __finished: dict = {}

    def __init__(self, mode: str) -> None:
        self.create_board()
        self.__fill_dict()
        self.set_number(mode)


    def __fill_dict(self) -> None:
        for char in range(9):
            self.__cells[ascii_uppercase[char]] = []
            self.__finished[ascii_uppercase[char]] = False

        for char in range(9):
            self.__cells[str(char)] = []
            self.__finished[str(char)] = False


    def create_board(self) -> None:
        self.__board = [[' ' for i in range(self.__size)] for j in range(self.__size)]


    def check_pos(self, number: int, pos: tuple, min: tuple, max: tuple) -> bool:
        is_in_col: bool = False
        is_in_row: bool = False
        is_in_group: bool = False

        is_in_col = True if number in self.__cells[ascii_uppercase[pos[0]]] else False

        is_in_row = True if number in self.__cells[str(pos[1])] else False

        for i in range(min[0], max[0]):
            for j in range(min[0], max[0]):
                if number == self.__board[j]:
                    is_in_group = True

        return True if (is_in_col is True) or (is_in_row is True) or (is_in_group is True) else False


    def fill_group(self, runs: int, qtt_number: int, info_col: tuple, info_row: tuple) -> None:
        min_col, max_col = info_col
        min_row, max_row = info_row
        while runs < qtt_number:
            pos_col = randint(min_col, max_col)
            pos_row = randint(min_row, max_row)
            num = randint(1,9)

            while self.check_pos(num, (pos_col,pos_row), (min_row, min_col), (max_row, max_col)) is True:
                num = randint(1,9)

            self.__board[pos_row][pos_col] = f'{Fore.GREEN}{num}{Fore.RESET}'
            self.__cells[ascii_uppercase[pos_col]].append(num)
            self.__cells[str(pos_row)].append(num)

            runs += 1


    def set_number(self, mode: str) -> None:
        qtt_number: int = 0

        if mode == 'easy':
            qtt_number = 3

        elif mode == 'medium':
            qtt_number = 2

        elif mode == 'hard':
            qtt_number = 1

        min_col, max_col = 0, 2
        min_row, max_row = 0, 2
        for i in range(3):
            for j in range(3):
                self.fill_group(0, qtt_number, (min_col, max_col), (min_row, max_row))
                min_col += 3
                max_col += 3
            min_col, max_col = 0, 0
            min_row += 3
            max_row += 3



    def show_board(self) -> None:
        header: list = []
        for c in range(self.__size):
            header.append(ascii_uppercase[c])

        print(tabulate(self.__board, tablefmt='fancy_grid', showindex=True, headers=header, numalign='center', stralign='center'))


    def change_to_num(self, pos: str) -> int:
        return ascii_uppercase.index(pos)


    def insert_number(self, cell: str, number: int) -> None:
        col = self.change_to_num(cell[0])
        row = cell[1]

        self.__board[int(row)][col] = number
        self.__cells[cell[0]].append(number)
        self.__cells[row].append(number)

    def change_number(self, cell: str, old: int, new: int) -> None:
        col = self.change_to_num(cell[0])
        row = cell[1]

        self.__board[int(row)][col] = new

        self.__cells[cell[0]][self.__cells[cell[0]].index(int(old))] = new
        self.__cells[row][self.__cells[row].index(int(old))] = new

    def remove_number(self, cell: str, number: int) -> None:
        col = self.change_to_num(cell[0])
        row = cell[1]

        self.__board[int(row)][col] = ' '
        self.__cells[cell[0]][self.__cells[cell[0]].index(int(number))] = ' '
        self.__cells[row][self.__cells[row].index(int(number))] = ' '


    def check_win(self) -> bool:
        finished = False
        for key in self.__finished:
            if self.__cells[key].sort() == ['1','2','3','4','5','6','7','8','9']:
                self.__finished[key] = True


        if False in self.__finished.values():
            finished = False
        else:
            finished = True

        return finished

    def main_loop(self) -> None:
        while True:
            if self.check_win() is True:
                print('Congratulations...')
                break

            system('clear')
            self.show_board()
            command = input('> ')

            if command.startswith('insert'):
                self.insert_number(command.split(' ')[1], command.split(' ')[2])

            if command.startswith('change'):
                print(command.split(' '))
                self.change_number(command.split(' ')[1], command.split(' ')[2], command.split(' ')[3])

            if command.startswith('remove'):
                self.remove_number(command.split(' ')[1], command.split(' ')[2])


if len(argv) == 1:
    print('To play game, use: python3 main.py [easy, medium, hard]')

else:
    g: Game = Game(argv[1])
    g.main_loop()
