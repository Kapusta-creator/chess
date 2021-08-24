import sys
import sqlite3
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QMovie, QColor, QPixmap
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer
from PyQt5.QtWidgets import QInputDialog
from menu import Ui_MainWindow
from our_game import Ui_our_game
from table_score import Ui_Form
from promote_pawn import Ui_Promote_form
from game_level import Ui_level
from functools import partial
from os import path

PARENT_DIR = path.dirname(path.abspath(__file__))
WHITE = 1
BLACK = 2
SHAH = False
MATE = False
STALEMATE = False
COOL_CATS = []
OLD_CATS = []
DEFAULT_PIECES = []
command = []
OUR_MUSIC = "country.mp3"
MUSIC = True
DEPTH = 3
AI_COLOR = BLACK
PLAYER_COLOR = WHITE
PROMOTING = False
AI_MOVE = False
GAME_MODE = 2
NICKNAME1 = "DemoPlayer"
NICKNAME2 = "AI"
CHESS_TYPE = 3
CHESS_NAME = "default_"
PAWN_EVAL_WHITE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
    [0.5, 1, 1, -2, -2, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0]]

PAWN_EVAL_BLACK = PAWN_EVAL_WHITE[::-1]

KNIGHT_EVAL = [
    [-5, -4, -3, -3, -3, -3, -4, -5],
    [-4, -2, 0, 0, 0, 0, -2, -4],
    [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
    [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
    [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
    [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
    [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]]

BISHOP_EVAL_WHITE = [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
    [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
    [-1, 0, 1, 1, 1, 1, 0, -1],
    [-1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]]

BISHOP_EVAL_BLACK = BISHOP_EVAL_WHITE[::-1]

ROOK_EVAL_WHITE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0.5, 1, 1, 1, 1, 1, 1, 0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [0, 0, 0, 0.5, 0.5, 0, 0, 0]]

ROOK_EVAL_BLACK = ROOK_EVAL_WHITE[::-1]

EVAL_QUEEN = [
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-1, 0, 0.5, 0, 0, 0, 0, -1],
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2]]

KING_EVAL_WHITE = [
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 3, 1, 0, 0, 1, 3, 2]]

KING_EVAL_BLACK = KING_EVAL_WHITE[::-1]


def opponent(color):  # возвращает цвет противника
    if color == WHITE:
        return BLACK
    return WHITE


def change_level(level):  # Меняет уровень сложности(глубину рекурсии шахматного алгоритма)
    global DEPTH
    DEPTH = level


def change_game_mode(game_mode):  # Меняет режим игры
    global GAME_MODE
    GAME_MODE = game_mode


def change_chess_type(c_type):  # Меняет тип фигурок
    global CHESS_TYPE
    CHESS_TYPE = c_type


def correct_coords(row, col):  # Проверка координат на правильность
    return 0 <= row < 8 and 0 <= col < 8


def get_base():  # Возвращает словарь по базе данных,
    con = sqlite3.connect("db/ScoreTable.db")  # ключи - имена игроков, значения - текущий рейтинг
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM Gamers""").fetchall()
    con.close()
    rating = {}
    for i in result:
        rating[i[0]] = i[1]
    return rating


def insert_to_base(nickname):  # Добавляет новый никнейм в базу
    con = sqlite3.connect("db/ScoreTable.db")
    cur = con.cursor()
    result = cur.execute("""INSERT INTO Gamers VALUES(?, ?)""", (nickname, 0)).fetchall()
    con.commit()
    con.close()


def update_rate(new_rate, nickname):  # Обновляет рейтинг в базе
    con = sqlite3.connect("db/ScoreTable.db")
    cur = con.cursor()
    result = cur.execute("""UPDATE Gamers SET Rate = ?
                            WHERE Nickname = ?""", (max(0, int(new_rate)), nickname)).fetchall()
    con.commit()
    con.close()


def get_coeff(rate):  # Рассчет коэффициента при добавлении рейтинга
    if rate >= 2400:
        return 10
    elif rate < 2400 and rate > 1000:
        return 20
    else:
        return 30


class Menu(QMainWindow, Ui_MainWindow):  # Класс главного меню
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        for i in self.buttonGroup.buttons():
            i.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        self.man_vs_man.clicked.connect(partial(self.game_mode, 1))
        self.man_vs_pc.clicked.connect(partial(self.game_mode, 2))
        self.old_cats.clicked.connect(partial(self.chess_type, 1))
        self.standart.clicked.connect(partial(self.chess_type, 2))
        self.new_cats.clicked.connect(partial(self.chess_type, 3))
        self.sound.clicked.connect(self.play_music)
        self.play.clicked.connect(self.chess)
        self.table.clicked.connect(self.show_table)
        self.sound_label.setPixmap(QPixmap("pics/sound_off.png"))
        self.load_mp3(path.join(PARENT_DIR, "sound", OUR_MUSIC))
        self.human_vs_ai.show()
        self.human_vs_human.hide()
        self.default_circle.show()
        self.old_cats_circle.hide()
        self.cool_cats_circle.hide()
        self.statusBar().hide()

    def load_mp3(self, filename):  # Загружаем музыку
        self.player = QMediaPlayer()
        playlist = QMediaPlaylist(self.player)
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        playlist.addMedia(content)
        playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.player.setPlaylist(playlist)

    def play_music(self):  # Флексим(Запускаем музыку)
        global MUSIC
        if MUSIC:
            self.sound_label.setPixmap(QPixmap("pics/sound_on.png"))
            self.player.play()
        else:
            self.sound_label.setPixmap(QPixmap("pics/sound_off.png"))
            self.player.stop()
        MUSIC = not MUSIC

    def game_mode(self, game_mode):  # Замена режима игры(в меню)
        change_game_mode(game_mode)
        if game_mode == 1:
            self.human_vs_human.show()
            self.human_vs_ai.hide()
        else:
            self.human_vs_human.hide()
            self.human_vs_ai.show()

    def chess_type(self, c_type):  # Замена типа фигурок(в меню)
        change_chess_type(c_type)
        if c_type == 1:
            global CHESS_NAME
            CHESS_NAME = "old_"
            self.old_cats_circle.show()
            self.cool_cats_circle.hide()
            self.default_circle.hide()
        elif c_type == 2:
            CHESS_NAME = "default_"
            self.old_cats_circle.hide()
            self.cool_cats_circle.hide()
            self.default_circle.show()
        else:
            CHESS_NAME = "cool_"
            self.cool_cats_circle.show()
            self.old_cats_circle.hide()
            self.default_circle.hide()

    def run(self, text):  # Диалоговое окно для ввода никнейма
        name, ok_pressed = QInputDialog.getText(self, "Введите свой никнейм", f"{text}")
        if ok_pressed:
            if name == "AI":
                name = "Жулик"
            elif name == "":
                name = "DemoPlayer"
            return name
        else:
            return ""

    def chess(self):  # Запуск игры
        global NICKNAME1, NICKNAME2
        database = get_base()
        nicknames = list(database.keys())
        if GAME_MODE == 2:
            NICKNAME1 = self.run("Как вас зовут?")
            if NICKNAME1 == "":
                return 0
            if NICKNAME1 not in nicknames:
                insert_to_base(NICKNAME1)
        else:
            NICKNAME1 = self.run("Кто будет играть за белых?")
            if NICKNAME1 == "":
                return 0
            if NICKNAME1 not in nicknames:
                insert_to_base(NICKNAME1)
            NICKNAME2 = self.run("Кто будет играть за черных?")
            if NICKNAME2 == "":
                return 0
            if NICKNAME2 not in nicknames:
                insert_to_base(NICKNAME2)
        global DEPTH
        DEPTH = 3
        self.level = Level()
        if GAME_MODE == 2:
            self.level.show()
        else:
            self.game = Game()
            self.game.show()

    def show_table(self):  # Показать таблицу лидеров
        self.rate_table = ScoreTable()
        self.rate_table.show()


class Board:  # Класс шахматной доски
    def __init__(self, our_field):
        self.color = WHITE
        self.Kings_Coord = [(7, 4), (0, 4)]
        self.last_move = [(0, 0), (0, 0)]
        if type(our_field) == int:
            self.field = []
            for row in range(8):
                self.field.append([None] * 8)
            self.field[6] = [Pawn(PLAYER_COLOR), Pawn(PLAYER_COLOR), Pawn(PLAYER_COLOR),
                             Pawn(PLAYER_COLOR),
                             Pawn(PLAYER_COLOR), Pawn(PLAYER_COLOR), Pawn(PLAYER_COLOR),
                             Pawn(PLAYER_COLOR)]
            self.field[1] = [Pawn(AI_COLOR), Pawn(AI_COLOR), Pawn(AI_COLOR), Pawn(AI_COLOR),
                             Pawn(AI_COLOR), Pawn(AI_COLOR), Pawn(AI_COLOR), Pawn(AI_COLOR)]
            self.field[7][7] = Rook(PLAYER_COLOR)
            self.field[7][0] = Rook(PLAYER_COLOR)
            self.field[0][7] = Rook(AI_COLOR)
            self.field[0][0] = Rook(AI_COLOR)
            self.field[7][1] = Knight(PLAYER_COLOR)
            self.field[7][6] = Knight(PLAYER_COLOR)
            self.field[0][1] = Knight(AI_COLOR)
            self.field[0][6] = Knight(AI_COLOR)
            self.field[7][2] = Bishop(PLAYER_COLOR)
            self.field[7][5] = Bishop(PLAYER_COLOR)
            self.field[0][2] = Bishop(AI_COLOR)
            self.field[0][5] = Bishop(AI_COLOR)
            self.field[7][3] = Queen(PLAYER_COLOR)
            self.field[0][3] = Queen(AI_COLOR)
            self.field[7][4] = King(PLAYER_COLOR)
            self.field[0][4] = King(AI_COLOR)
        else:
            self.field = [[None for j in range(8)] for i in range(8)]
            for i in range(8):
                for j in range(8):
                    if our_field[i][j] is not None:
                        self.field[i][j] = eval(f"{our_field[i][j].__class__.__name__}"
                                                f"({our_field[i][j].get_color()})")
                    else:
                        self.field[i][j] = None
                    if self.field[i][j] is not None:
                        if self.field[i][j].__class__.__name__ == "King":
                            if self.field[i][j].get_color() == WHITE:
                                self.Kings_Coord[0] = (i, j)
                            else:
                                self.Kings_Coord[1] = (i, j)
        self.legal_moves = []
        self.piece = None
        self.enemy = None

    def is_under_attack(self, row, col, color):  # Проверить, под атакой ли клетка
        for i in range(8):
            for j in range(8):
                if self.field[i][j] is not None:
                    if self.field[i][j].get_color() != color:
                        if self.field[i][j].can_attack(self, i, j, row, col):
                            return True
        return False

    def update_it(self, Sa_White, Sa_Black):  # Обновление рейтинга
        database = get_base()
        if NICKNAME2 == "AI":
            if DEPTH == 2:
                Rblack = min(150, database[NICKNAME2])
            elif DEPTH == 3:
                Rblack = min(300, database[NICKNAME2])
            else:
                Rblack = database[NICKNAME2]
        else:
            Rblack = database[NICKNAME2]
        Rwhite = database[NICKNAME1]
        Kblack = get_coeff(Rblack)
        Kwhite = get_coeff(Rwhite)
        EaBlack = 1 / (1 + 10 ** ((Rwhite - Rblack) / 400))
        EaWhite = 1 / (1 + 10 ** ((Rblack - Rwhite) / 400))
        update_rate(Rwhite + Kwhite * (Sa_White - EaWhite), NICKNAME1)
        update_rate(Rblack + Kblack * (Sa_Black - EaBlack), NICKNAME2)

    def shah(self):  # Проверка на шах
        global MATE
        if self.is_under_attack(self.Kings_Coord[opponent(self.color) - 1][0],
                                self.Kings_Coord[opponent(self.color) - 1][1],
                                opponent(self.color)):
            global SHAH
            SHAH = True
            if self.check_mate(opponent(self.color)):
                MATE = True
                if opponent(self.color) == BLACK:
                    Sa_Black = 0
                    Sa_White = 1
                else:
                    Sa_White = 0
                    Sa_Black = 1
                self.update_it(Sa_White, Sa_Black)
        else:
            if self.check_mate(opponent(self.color)):
                MATE = True
                global STALEMATE
                STALEMATE = True
                self.update_it(0.5, 0.5)
                return 0

    def get_piece(self, row, col):  # Возвращает бъект из клетки поля
        return self.field[row][col]

    def move_piece(self, row, col, row1, col1):  # Передвинуть фигурку на доске
        piece = self.field[row][col]
        if piece.__class__.__name__ == "King":
            if self.color == WHITE:
                self.Kings_Coord[0] = (row1, col1)
            else:
                self.Kings_Coord[1] = (row1, col1)
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.shah()
        self.color = opponent(self.color)
        self.field[row1][col1].moves += 1

    def ugly(self, row, col, row1, col1):  # Симулировать ход
        self.last_move = [(row, col), (row1, col1)]
        ugly_piece = self.field[row][col]
        self.field[row][col] = None
        self.field[row1][col1] = ugly_piece

    def ugly_undo(self, row, col, row1, col1, enemy, piece):  # Отмена хода
        self.field[row][col] = piece
        self.field[row1][col1] = enemy

    def check_mate(self, color):  # Проверка на мат
        for i in range(8):
            for j in range(8):
                if self.field[i][j] is not None:
                    if self.field[i][j].get_color() == color:
                        self.check_legal_moves(self.field[i][j], i, j)
        if len(self.legal_moves) == 0:
            return True
        else:
            self.legal_moves = []
            return False

    def change_position_from_check(self, row, col, row1, col1, king):  # Симулировать ход для
        self.enemy = self.field[row1][col1]                            # проверки возможности хода
        self.piece = self.field[row][col]
        self.field[row1][col1] = self.piece
        self.field[row][col] = None
        result = not self.is_under_attack(*king, self.piece.get_color())
        self.field[row1][col1] = self.enemy
        self.field[row][col] = self.piece
        return result

    def check_legal_moves(self, piece, i, j):  # Посмотреть возможные ходы
        color = piece.get_color()
        if piece.__class__.__name__ == "Pawn":
            if color == BLACK:
                movement = 1
            else:
                movement = -1
            if (correct_coords(i + movement, j) and
                    self.field[i][j].can_move(self, i, j, i + movement, j)):
                if self.change_position_from_check(i, j, i + movement, j,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i + movement, j])
            if (correct_coords(i + 2 * movement, j) and
                    self.field[i][j].can_move(self, i, j, i + 2 * movement, j)):
                if self.change_position_from_check(i, j, i + 2 * movement, j,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i + 2 * movement, j])
            if (correct_coords(i + movement, j + 1) and
                    self.field[i][j].can_attack(self, i, j, i + movement, j + 1)):
                if self.change_position_from_check(i, j, i + movement, j + 1,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i + movement, j + 1])
            if (correct_coords(i + movement, j - 1) and
                    self.field[i][j].can_attack(self, i, j, i + movement, j - 1)):
                if self.change_position_from_check(i, j, i + movement, j - 1,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i + movement, j - 1])
        elif piece.__class__.__name__ == "Rook":
            for k in range(i + 1, 8):
                if self.field[i][j].can_move(self, i, j, k, j):
                    if self.change_position_from_check(i, j, k, j,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k, j])
                else:
                    break
            for k in range(i - 1, -1, -1):
                if self.field[i][j].can_move(self, i, j, k, j):
                    if self.change_position_from_check(i, j, k, j,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k, j])
                else:
                    break
            for k in range(j + 1, 8):
                if self.field[i][j].can_move(self, i, j, i, k):
                    if self.change_position_from_check(i, j, i, k,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, i, k])
                else:
                    break
            for k in range(j - 1, -1, -1):
                if self.field[i][j].can_move(self, i, j, i, k):
                    if self.change_position_from_check(i, j, i, k,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, i, k])
                else:
                    break
        elif piece.__class__.__name__ == "Bishop":
            k = i
            m = j
            while k != 7 and m != 7:
                if self.field[i][j].can_move(self, i, j, k + 1, m + 1):
                    if self.change_position_from_check(i, j, k + 1, m + 1,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k + 1, m + 1])
                else:
                    break
                k += 1
                m += 1

            k = i
            m = j
            while k != 0 and m != 0:
                if self.field[i][j].can_move(self, i, j, k - 1, m - 1):
                    if self.change_position_from_check(i, j, k - 1, m - 1,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k - 1, m - 1])
                else:
                    break
                k -= 1
                m -= 1
            k = i
            m = j
            while k != 7 and m != 0:
                if self.field[i][j].can_move(self, i, j, k + 1, m - 1):
                    if self.change_position_from_check(i, j, k + 1, m - 1,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k + 1, m - 1])
                else:
                    break
                k += 1
                m -= 1
            k = i
            m = j
            while k != 0 and m != 7:
                if self.field[i][j].can_move(self, i, j, k - 1, m + 1):
                    if self.change_position_from_check(i, j, k - 1, m + 1,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k - 1, m + 1])
                else:
                    break
                k -= 1
                m += 1
        elif piece.__class__.__name__ == "Knight":
            if (correct_coords(i - 2, j + 1) and
                    self.field[i][j].can_move(self, i, j, i - 2, j + 1)):
                if self.change_position_from_check(i, j, i - 2, j + 1,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i - 2, j + 1])
            if (correct_coords(i - 2, j - 1) and
                    self.field[i][j].can_move(self, i, j, i - 2, j - 1)):
                if self.change_position_from_check(i, j, i - 2, j - 1,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i - 2, j - 1])
            if (correct_coords(i + 2, j + 1) and
                    self.field[i][j].can_move(self, i, j, i + 2, j + 1)):
                if self.change_position_from_check(i, j, i + 2, j + 1,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i + 2, j + 1])
            if (correct_coords(i + 2, j - 1) and
                    self.field[i][j].can_move(self, i, j, i + 2, j - 1)):
                if self.change_position_from_check(i, j, i + 2, j - 1,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i + 2, j - 1])
            if (correct_coords(i - 1, j + 2) and
                    self.field[i][j].can_move(self, i, j, i - 1, j + 2)):
                if self.change_position_from_check(i, j, i - 1, j + 2,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i - 1, j + 2])
            if (correct_coords(i - 1, j - 2) and
                    self.field[i][j].can_move(self, i, j, i - 1, j - 2)):
                if self.change_position_from_check(i, j, i - 1, j - 2,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i - 1, j - 2])
            if (correct_coords(i + 1, j + 2) and
                    self.field[i][j].can_move(self, i, j, i + 1, j + 2)):
                if self.change_position_from_check(i, j, i + 1, j + 2,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i + 1, j + 2])
            if (correct_coords(i + 1, j - 2) and
                    self.field[i][j].can_move(self, i, j, i + 1, j - 2)):
                if self.change_position_from_check(i, j, i + 1, j - 2,
                                                   self.Kings_Coord[color - 1]):
                    self.legal_moves.append([i, j, i + 1, j - 2])
        elif piece.__class__.__name__ == "Queen":
            k = i
            m = j
            while k != 7 and m != 7:
                if self.field[i][j].can_move(self, i, j, k + 1, m + 1):
                    if self.change_position_from_check(i, j, k + 1, m + 1,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k + 1, m + 1])
                else:
                    break
                k += 1
                m += 1

            k = i
            m = j
            while k != 0 and m != 0:
                if self.field[i][j].can_move(self, i, j, k - 1, m - 1):
                    if self.change_position_from_check(i, j, k - 1, m - 1,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k - 1, m - 1])
                else:
                    break
                k -= 1
                m -= 1
            k = i
            m = j
            while k != 7 and m != 0:
                if self.field[i][j].can_move(self, i, j, k + 1, m - 1):
                    if self.change_position_from_check(i, j, k + 1, m - 1,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k + 1, m - 1])
                else:
                    break
                k += 1
                m -= 1
            k = i
            m = j
            while k != 0 and m != 7:
                if self.field[i][j].can_move(self, i, j, k - 1, m + 1):
                    if self.change_position_from_check(i, j, k - 1, m + 1,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k - 1, m + 1])
                else:
                    break
                k -= 1
                m += 1
            for k in range(i, 8):
                if self.field[i][j].can_move(self, i, j, k, j):
                    if self.change_position_from_check(i, j, k, j,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k, j])
                else:
                    break
            for k in range(i + 1, 8):
                if self.field[i][j].can_move(self, i, j, k, j):
                    if self.change_position_from_check(i, j, k, j,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k, j])
                else:
                    break
            for k in range(i - 1, -1, -1):
                if self.field[i][j].can_move(self, i, j, k, j):
                    if self.change_position_from_check(i, j, k, j,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, k, j])
                else:
                    break
            for k in range(j + 1, 8):
                if self.field[i][j].can_move(self, i, j, i, k):
                    if self.change_position_from_check(i, j, i, k,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, i, k])
                else:
                    break
            for k in range(j - 1, -1, -1):
                if self.field[i][j].can_move(self, i, j, i, k):
                    if self.change_position_from_check(i, j, i, k,
                                                       self.Kings_Coord[color - 1]):
                        self.legal_moves.append([i, j, i, k])
                else:
                    break
        elif piece.__class__.__name__ == "King":
            if correct_coords(i + 1, j + 1) and self.field[i][j].can_move(self, i, j, i + 1, j + 1):
                if self.change_position_from_check(i, j, i + 1, j + 1,
                                                   (i + 1, j + 1)):
                    self.legal_moves.append([i, j, i + 1, j + 1])
            if correct_coords(i + 1, j - 1) and self.field[i][j].can_move(self, i, j, i + 1, j - 1):
                if self.change_position_from_check(i, j, i + 1, j - 1,
                                                   (i + 1, j - 1)):
                    self.legal_moves.append([i, j, i + 1, j - 1])
            if correct_coords(i + 1, j) and self.field[i][j].can_move(self, i, j, i + 1, j):
                if self.change_position_from_check(i, j, i + 1, j,
                                                   (i + 1, j)):
                    self.legal_moves.append([i, j, i + 1, j])
            if correct_coords(i, j + 1) and self.field[i][j].can_move(self, i, j, i, j + 1):
                if self.change_position_from_check(i, j, i, j + 1,
                                                   (i, j + 1)):
                    self.legal_moves.append([i, j, i, j + 1])
            if correct_coords(i, j - 1) and self.field[i][j].can_move(self, i, j, i, j - 1):
                if self.change_position_from_check(i, j, i, j - 1,
                                                   (i, j - 1)):
                    self.legal_moves.append([i, j, i, j - 1])
            if correct_coords(i - 1, j + 1) and self.field[i][j].can_move(self, i, j, i - 1, j + 1):
                if self.change_position_from_check(i, j, i - 1, j + 1,
                                                   (i - 1, j + 1)):
                    self.legal_moves.append([i, j, i - 1, j + 1])
            if correct_coords(i - 1, j) and self.field[i][j].can_move(self, i, j, i - 1, j):
                if self.change_position_from_check(i, j, i - 1, j,
                                                   (i - 1, j)):
                    self.legal_moves.append([i, j, i - 1, j])
            if correct_coords(i - 1, j - 1) and self.field[i][j].can_move(self, i, j, i - 1, j - 1):
                if self.change_position_from_check(i, j, i - 1, j - 1,
                                                   (i - 1, j - 1)):
                    self.legal_moves.append([i, j, i - 1, j - 1])

    def castling0(self):  # Рокировка влево
        global MATE
        if self.color == WHITE:
            row = 7
        else:
            row = 0
        if (self.field[row][4].__class__.__name__ == "King" and
                self.field[row][0].__class__.__name__ == "Rook" and
                self.field[row][4].moves == 0
                and self.field[row][0].moves == 0):
            if (self.field[row][1] is None
                    and self.field[row][2] is None and
                    self.field[row][3] is None and not self.rock_shah("left", row)):
                self.field[row][2] = self.field[row][4]
                self.field[row][4] = None
                self.field[row][3] = self.field[row][0]
                self.field[row][0] = None
                if self.is_under_attack(self.Kings_Coord[opponent(self.color) - 1][0],
                                        self.Kings_Coord[opponent(self.color) - 1][1],
                                        opponent(self.color)):
                    global SHAH
                    SHAH = True
                    if self.check_mate(opponent(self.color)):
                        MATE = True
                        if opponent(self.color) == BLACK:
                            Sa_Black = 0
                            Sa_White = 1
                        else:
                            Sa_White = 0
                            Sa_Black = 1
                        self.update_it(Sa_White, Sa_Black)
                else:
                    if self.check_mate(opponent(self.color)):
                        MATE = True
                        global STALEMATE
                        STALEMATE = True
                        self.update_it(0.5, 0.5)
                self.Kings_Coord[self.color - 1] = (row, 2)
                self.color = opponent(self.color)
                return True
        return False

    def castling7(self):  # Рокировка вправо
        global MATE
        if self.color == WHITE:
            row = 7
        else:
            row = 0
        if (self.field[row][4].__class__.__name__ == "King" and
                self.field[row][7].__class__.__name__ == "Rook" and
                self.field[row][4].moves == 0
                and self.field[row][7].moves == 0):
            if (self.field[row][5] is None
                    and self.field[row][6] is None and not self.rock_shah("right", row)):
                self.field[row][6] = self.field[row][4]
                self.field[row][4] = None
                self.field[row][5] = self.field[row][7]
                self.field[row][7] = None
                if self.is_under_attack(self.Kings_Coord[opponent(self.color) - 1][0],
                                        self.Kings_Coord[opponent(self.color) - 1][1],
                                        opponent(self.color)):
                    global SHAH
                    SHAH = True
                    if self.check_mate(opponent(self.color)):
                        MATE = True
                        if opponent(self.color) == BLACK:
                            Sa_Black = 0
                            Sa_White = 1
                        else:
                            Sa_White = 0
                            Sa_Black = 1
                        self.update_it(Sa_White, Sa_Black)
                else:
                    if self.check_mate(opponent(self.color)):
                        MATE = True
                        global STALEMATE
                        STALEMATE = True
                        self.update_it(0.5, 0.5)
                self.Kings_Coord[self.color - 1] = (row, 6)
                self.color = opponent(self.color)
                return True
        return False

    def rock_shah(self, side, row):  # Проверить, не подставится ли король после рокировки
        if side == "left":
            king = self.field[row][4]
            rook = self.field[row][0]
            self.field[row][2] = self.field[row][4]
            self.field[row][4] = None
            self.field[row][3] = self.field[row][0]
            self.field[row][0] = None
            result = self.is_under_attack(row, 2, self.color)
            self.field[row][2] = None
            self.field[row][4] = king
            self.field[row][3] = None
            self.field[row][0] = rook
            return result
        else:
            king = self.field[row][4]
            rook = self.field[row][7]
            self.field[row][6] = self.field[row][4]
            self.field[row][4] = None
            self.field[row][5] = self.field[row][7]
            self.field[row][7] = None
            result = self.is_under_attack(row, 6, self.color)
            self.field[row][4] = None
            self.field[row][4] = king
            self.field[row][5] = None
            self.field[row][7] = rook
            return result


def ugly_moves(board, color):  # Проверить все возможные ходы
    for i in range(8):
        for j in range(8):
            if board.field[i][j] is not None:
                if board.field[i][j].get_color() == color:
                    board.check_legal_moves(board.field[i][j], i, j)  # get all legal moves
    return board.legal_moves


def ugly_move(move, board):  # Симулировать ход на доске
    board.ugly(*move)


def undo(board, move, enemy, piece):  # Отмена хода
    board.ugly_undo(*move, enemy, piece)


def minimax_root(board, depth, color):  # Запуск перебора ходов
    newGameMoves = ugly_moves(board, color)
    board.legal_moves = []
    bestMove = -9999
    bestMovePiece = newGameMoves[0]
    for i in newGameMoves:
        row, col = i[0], i[1]
        row1, col1 = i[2], i[3]
        enemy = board.field[row1][col1]
        piece = board.field[row][col]
        ugly_move(i, board)
        value = minimax(depth - 1, board, -10000, 10000, opponent(color))
        undo(board, i, enemy, piece)
        if value >= bestMove:
            bestMove = value
            bestMovePiece = i
    return bestMovePiece


def minimax(depth, board, alpha, beta, color):  # Работа с деревом ходов
    if not depth:
        return -evaluateBoard(board)
    newGameMoves = ugly_moves(board, color)
    board.legal_moves = []
    if color == AI_COLOR:
        best_move = -9999
        for i in newGameMoves:
            row, col = i[0], i[1]
            row1, col1 = i[2], i[3]
            enemy = board.field[row1][col1]
            piece = board.field[row][col]
            ugly_move(i, board)
            best_move = max([best_move, minimax(depth - 1, board, alpha, beta, opponent(color))])
            undo(board, i, enemy, piece)
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    else:
        best_move = 9999
        for i in newGameMoves:
            row, col = i[0], i[1]
            row1, col1 = i[2], i[3]
            enemy = board.field[row1][col1]
            piece = board.field[row][col]
            ugly_move(i, board)
            best_move = min([best_move, minimax(depth - 1, board, alpha, beta, opponent(color))])
            undo(board, i, enemy, piece)
            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move
        return best_move


def evaluateBoard(board):  # Рассчитать стоимость доски
    totalEvaluation = 0
    for i in range(8):
        for j in range(8):
            totalEvaluation = totalEvaluation + getPieceValue(board.field[i][j], i, j)
    return totalEvaluation


def getAbsoluteValue(piece, i, j):  # Рассчет стоимости фигуры на доске
    if piece.__class__.__name__ == "Pawn":
        return 10 + PAWN_EVAL_WHITE[j][i] if piece.get_color() == WHITE else PAWN_EVAL_BLACK[j][i]
    if piece.__class__.__name__ == "Rook":
        return 50 + ROOK_EVAL_WHITE[j][i] if piece.get_color() == WHITE else ROOK_EVAL_BLACK[j][i]
    if piece.__class__.__name__ == "Knight":
        return 30 + KNIGHT_EVAL[j][i]
    if piece.__class__.__name__ == "Bishop":
        return (30 + BISHOP_EVAL_WHITE[j][i] if piece.get_color() ==
                                                WHITE else BISHOP_EVAL_BLACK[j][i])
    if piece.__class__.__name__ == "Queen":
        return 90 + EVAL_QUEEN[j][i]
    if piece.__class__.__name__ == "King":
        return 900 + KING_EVAL_WHITE[j][i] if piece.get_color() == WHITE else KING_EVAL_BLACK[j][i]


def getPieceValue(piece, i, j):  # Возвращает стоимость фигуры
    if piece == None:
        return 0
    absolute_value = getAbsoluteValue(piece, i, j)
    return absolute_value if piece.get_color() == WHITE else -absolute_value


class Game(QWidget, Ui_our_game):  # Класс основной игры
    def __init__(self):
        global STALEMATE, SHAH, MATE
        super().__init__()
        self.setupUi(self)
        STALEMATE = False
        SHAH = False
        MATE = False
        self.cells = self.buttonGroup.buttons()
        self.board = Board(1)
        self.castling_left.clicked.connect(self.castling0)
        self.castling_right.clicked.connect(self.castling7)
        for i in range(len(self.cells)):
            if (i + i // 8) % 2:
                self.cells[i].setStyleSheet("background-color: rgba(171, 162, 154, 255)")
            else:
                self.cells[i].setStyleSheet("background-color: rgba(242, 222, 208, 255)")
            if self.board.field[i // 8][i % 8] is not None:
                self.cells[i].setIcon(self.board.field[i // 8][i % 8].icon)
            self.cells[i].row = i // 8
            self.cells[i].col = i % 8
            self.cells[i].clicked.connect(partial(self.move, self.cells[i].row, self.cells[i].col))

    def promote_pawn(self, row, col):
        self.promote_it = PromotePawn(self.board, row, col, self)
        self.promote_it.show()

    def move_piece(self, row, col, row1, col1):  # Сделать ход
        global STALEMATE, SHAH, MATE
        self.board.move_piece(row, col, row1, col1)
        self.menyaem(row, col, row1, col1)
        if self.board.field[row1][col1].__class__.__name__ == "Pawn" and (row1 == 0 or row1 == 7):
            if opponent(self.board.color) == AI_COLOR and GAME_MODE == 2:
                self.board.field[row1][col1] = Queen(AI_COLOR)
                self.cells[row1 * 8 + col1].setIcon(self.board.field[row1][col1].icon)
            else:
                global PROMOTING
                PROMOTING = True
                self.promote_pawn(row1, col1)
        if STALEMATE:
            self.mate.setPixmap(QPixmap("pics/stalemate.png"))
            self.mate.show()
        elif MATE:
            self.mate.setPixmap(QPixmap("pics/mate.png"))
            self.mate.show()
        elif SHAH:
            self.mate.setPixmap(QPixmap("pics/Shah.png"))
            self.mate.show()
            SHAH = False
        else:
            self.mate.hide()

    def menyaem(self, row, col, row1, col1):  # Переставляем фигуру на доске
        self.cells[row1 * 8 + col1].setIcon(self.board.field[row1][col1].icon)
        self.cells[row * 8 + col].setIcon(QIcon())

    def pokras_lampas(self):  # Красим Доску в основные цвета
        for k in range(len(self.cells)):
            if (k + k // 8) % 2:
                self.cells[k].setStyleSheet("background-color: rgba(171, 162, 154, 255)")
            else:
                self.cells[k].setStyleSheet("background-color: rgba(242, 222, 208, 255)")

    def move(self, i, j):  # Принимаем команду на ход
        global command
        command += [i, j]
        if len(command) == 2:
            piece = self.board.field[i][j]
            if not piece is None:
                if piece.get_color() == self.board.color:
                    self.board.check_legal_moves(piece, i, j)
                    for k in self.board.legal_moves:
                        self.cells[k[2] * 8 + k[3]].setStyleSheet("background-color:"
                                                                  " rgba(255, 112, 112, 255)")
                else:
                    command = []
            else:
                command = []
        else:
            if command in self.board.legal_moves:
                self.pokras_lampas()
                self.board.legal_moves = []
                self.move_piece(*command)
                self.repaint()
                command = []
                global PROMOTING
                global MATE
                if not PROMOTING and not MATE and GAME_MODE == 2:
                    self.move_piece(*self.get_best_move())
            else:
                self.pokras_lampas()
                self.board.legal_moves = []
                piece = self.board.field[i][j]
                if not piece is None:
                    if piece.get_color() == self.board.color:
                        command = [command[2], command[3]]
                        self.board.check_legal_moves(piece, *command)
                        for k in self.board.legal_moves:
                            self.cells[k[2] * 8 + k[3]].setStyleSheet("background-color:"
                                                                      " rgba(255, 112, 112, 255)")
                    else:
                        command = []
                else:
                    command = []

    def get_best_move(self):  # Получаем ход ИИ
        game = Board(self.board.field)
        game.color = self.board.color
        bestMove = minimax_root(game, DEPTH, self.board.color)
        return bestMove

    def castling0(self):  # Рокировка влево
        if self.board.color == WHITE:
            row = 7
        else:
            row = 0
        if self.board.castling0():
            self.cells[row * 8 + 2].setIcon(self.board.field[row][2].icon)
            self.cells[row * 8 + 3].setIcon(self.board.field[row][3].icon)
            self.cells[row * 8 + 4].setIcon(QIcon())
            self.cells[row * 8 + 0].setIcon(QIcon())
            if NICKNAME2 == "AI":
                self.repaint()
                if not PROMOTING and not MATE and GAME_MODE == 2:
                    self.move_piece(*self.get_best_move())

    def castling7(self):  # Рокировка вправо
        if self.board.color == WHITE:
            row = 7
        else:
            row = 0
        if self.board.castling7():
            self.cells[row * 8 + 6].setIcon(self.board.field[row][6].icon)
            self.cells[row * 8 + 5].setIcon(self.board.field[row][5].icon)
            self.cells[row * 8 + 4].setIcon(QIcon())
            self.cells[row * 8 + 7].setIcon(QIcon())
            if NICKNAME2 == "AI":
                self.repaint()
                if not PROMOTING and not MATE and GAME_MODE == 2:
                    self.move_piece(*self.get_best_move())


class ScoreTable(QWidget, Ui_Form):  # класс таблица лидеров
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        goose = QMovie(path.join(PARENT_DIR, "pics", "goose.gif"))
        self.Goose.setMovie(goose)
        goose.start()
        cow = QMovie(path.join(PARENT_DIR, "pics", "cow.gif"))
        self.Cow.setMovie(cow)
        cow.start()
        cat = QMovie(path.join(PARENT_DIR, "pics", "cat.gif"))
        self.Cat.setMovie(cat)
        cat.start()
        dog = QMovie(path.join(PARENT_DIR, "pics", "dog.gif"))
        self.Dog.setMovie(dog)
        dog.start()
        self.loadTable()

    def loadTable(self):
        con = sqlite3.connect("db/ScoreTable.db")
        cur = con.cursor()
        database = cur.execute("""SELECT * FROM Gamers""").fetchall()
        con.close()
        database = sorted(database, key=lambda x: x[1], reverse=True)
        prizes = [[] for i in range(3)]
        if len(database) > 0:
            last = 0
            maxm = database[0][1]
            for i in range(len(database)):
                if database[i][1] == maxm:
                    prizes[last].append(i)
                else:
                    last += 1
                    if last > 2:
                        break
                    else:
                        prizes[last].append(i)
                        maxm = database[i][1]
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Имя", "Рейтинг"])
        self.tableWidget.setRowCount(0)
        stylesheet = "::section{Background-color:rgb(249,228,211);}"
        self.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        self.tableWidget.verticalHeader().setStyleSheet(stylesheet)
        for i in range(len(database)):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(database[i][0]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(database[i][1])))
            flag = False
            if i in prizes[0]:
                color = "#ffd700"
                flag = True
            elif i in prizes[1]:
                color = "#c0c0c0"
                flag = True
            elif i in prizes[2]:
                color = "#cd7f32"
                flag = True
            if flag:
                for j in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(i, j).setBackground(QColor(color))
        self.tableWidget.resizeColumnsToContents()


class PromotePawn(QWidget, Ui_Promote_form):  # класс превращение пешки
    def __init__(self, board, row, col, window):
        super().__init__()
        self.setupUi(self)
        self.board = board
        self.row = row
        self.col = col
        self.window = window
        self.window.setEnabled(False)
        self.color = self.board.field[self.row][self.col].get_color()
        self.promote_to_queen.setIcon(Queen(self.color).icon)
        self.promote_to_knight.setIcon(Knight(self.color).icon)
        self.promote_to_rook.setIcon(Rook(self.color).icon)
        self.promote_to_bishop.setIcon(Bishop(self.color).icon)
        self.promote_to_queen.clicked.connect(self.promote_to_q)
        self.promote_to_knight.clicked.connect(self.promote_to_k)
        self.promote_to_rook.clicked.connect(self.promote_to_r)
        self.promote_to_bishop.clicked.connect(self.promote_to_b)

    def enable(self):
        global PROMOTING
        self.window.setEnabled(True)
        PROMOTING = False
        self.board.color = self.color
        self.board.shah()
        self.board.color = opponent(self.color)
        if GAME_MODE == 2:
            self.window.move_piece(*self.window.get_best_move())
        self.close()

    def promote_to_q(self):
        self.board.field[self.row][self.col] = Queen(self.color)
        self.new_icon()
        self.enable()

    def promote_to_k(self):
        self.board.field[self.row][self.col] = Knight(self.color)
        self.new_icon()
        self.enable()

    def promote_to_r(self):
        self.board.field[self.row][self.col] = Rook(self.color)
        self.new_icon()
        self.enable()

    def promote_to_b(self):
        self.board.field[self.row][self.col] = Bishop(self.color)
        self.new_icon()
        self.enable()

    def new_icon(self):
        self.window.cells[self.row * 8 + self.col].setIcon(
            self.board.field[self.row][self.col].icon)


class Level(QWidget, Ui_level):  # Класс уровня сложности
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.easy.clicked.connect(partial(change_level, 2))
        self.medium.clicked.connect(partial(change_level, 3))
        self.hard.clicked.connect(partial(change_level, 4))
        self.medium.setChecked(True)
        self.ok.clicked.connect(self.start_game)

    def start_game(self):
        self.game = Game()
        self.game.show()
        self.close()

# Далее идёт описание классов отдельных фигур, методы классов выполняют одинаковые функции


class Queen:
    def __init__(self, color):
        self.color = color
        if self.color == WHITE:
            self.icon = QIcon("pics/" + CHESS_NAME + "wqueen.png")
        else:
            self.icon = QIcon("pics/" + CHESS_NAME + "bqueen.png")
        self.moves = 0

    def char(self):  # Получить символ фигуры
        return 'Q'

    def get_color(self):  # Получить цвет фигуры
        return self.color

    def can_move(self, board, row, col, row1, col1):  # Проверить возможность хода
        if not (board.get_piece(row1, col1) is None):
            if board.get_piece(row1, col1).get_color() != opponent(self.get_color()):
                return False
        type = 0
        if abs(col - col1) == abs(row - row1):
            type = 1
        else:
            if col1 != col:
                if row == row1:
                    type = 2
            else:
                type = 2
        if not type:
            return False
        if type == 1:
            stepr = 1 if row1 > row else -1
            stepc = 1 if col1 > col else -1
            c = col + stepc
            for r in range(row + stepr, row1, stepr):
                if not (board.get_piece(r, c) is None):
                    return False
                c += stepc
            return True
        else:
            if row1 != row and col1 != col:
                return False
            step = 1 if row1 >= row else -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False
            step = 1 if col1 >= col else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
            return True

    def can_attack(self, board, row, col, row1, col1):  # Проверить возможность атаки
        return self.can_move(board, row, col, row1, col1)


class Bishop:
    def __init__(self, color):
        self.color = color
        if self.color == WHITE:
            self.icon = QIcon("pics/" + CHESS_NAME + "wbishop.png")
        else:
            self.icon = QIcon("pics/" + CHESS_NAME + "bbishop.png")
        self.moves = 0

    def char(self):
        return 'B'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not (board.get_piece(row1, col1) is None):
            if board.get_piece(row1, col1).get_color() != opponent(self.get_color()):
                return False
        if abs(col - col1) != abs(row - row1):
            return False
        stepr = 1 if row1 > row else -1
        stepc = 1 if col1 > col else -1
        c = col + stepc
        for r in range(row + stepr, row1, stepr):
            if not (board.get_piece(r, c) is None):
                return False
            c += stepc
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Knight:
    def __init__(self, color):
        self.color = color
        if self.color == WHITE:
            self.icon = QIcon("pics/" + CHESS_NAME + "wknight.png")
        else:
            self.icon = QIcon("pics/" + CHESS_NAME + "bknight.png")
        self.moves = 0

    def char(self):
        return 'N'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not (board.get_piece(row1, col1) is None):
            if board.get_piece(row1, col1).get_color() != opponent(self.get_color()):
                return False
        if row + 2 == row1 or row - 2 == row1:
            if col + 1 == col1 or col - 1 == col1:
                return True
            return False
        else:
            if col + 2 == col1 or col - 2 == col1:
                if row + 1 == row1 or row - 1 == row1:
                    return True
                return False
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    def __init__(self, color):
        self.color = color
        if self.color == WHITE:
            self.icon = QIcon("pics/" + CHESS_NAME + "wking.png")
        else:
            self.icon = QIcon("pics/" + CHESS_NAME + "bking.png")
        self.moves = 0

    def char(self):
        return "K"

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not (board.get_piece(row1, col1) is None):
            if board.get_piece(row1, col1).get_color() != opponent(self.get_color()):
                return False
        if abs(row1 - row) > 1 or abs(col1 - col) > 1 or row1 == row and col1 == col:
            return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:
    def __init__(self, color):
        self.color = color
        if self.color == WHITE:
            self.icon = QIcon("pics/" + CHESS_NAME + "wpawn.png")
        else:
            self.icon = QIcon("pics/" + CHESS_NAME + "bpawn.png")
        self.moves = 0

    def char(self):
        return 'P'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if board.field[row1][col1] is not None:
            return False
        if col != col1:
            return False
        if self.color == BLACK:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        if row + direction == row1:
            return True
        if row == start_row and row + 2 * direction == row1 and \
                board.field[row + direction][col] is None:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        if board.field[row1][col1] is not None:
            if board.get_piece(row1, col1).get_color() != opponent(self.get_color()):
                return False
            direction = 1 if self.color == BLACK else -1
            return row + direction == row1 and abs(col - col1) == 1
        else:
            return False


class Rook:
    def __init__(self, color):
        self.color = color
        if self.color == WHITE:
            self.icon = QIcon("pics/" + CHESS_NAME + "wrook.png")
        else:
            self.icon = QIcon("pics/" + CHESS_NAME + "brook.png")
        self.moves = 0

    def char(self):
        return 'R'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not (board.get_piece(row1, col1) is None):
            if board.get_piece(row1, col1).get_color() != opponent(self.get_color()):
                return False
        if row1 != row and col1 != col:
            return False
        if row == row1 and col == col1:
            return False
        step = 1 if row1 >= row else -1
        for r in range(row + step, row1, step):
            if not (board.field[r][col] is None):
                return False
        step = 1 if col1 >= col else -1
        for c in range(col + step, col1, step):
            if not (board.field[row][c] is None):
                return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

# Здесь заканчивается описание классов фигур


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
