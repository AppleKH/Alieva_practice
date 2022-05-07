import tkinter
import tkinter.messagebox
import random
import timer


class Minesweeper(tkinter.Frame):
    COLUMNS = range(8, 41)
    ROWS = range(8, 21)
    MIN_MINES = 10

    TIMER_WIDTH = 3
    COUNT_WIDTH = 4

    EASY = (10,10,10)
    MEDIUM = (16,16,40)
    HARD = (30,15,80)

    @staticmethod
    def max_mines(columns, rows):
        return int(columns * rows * 0.9)

    def __init__(self, master):
        super().__init__(master)

        self.__first_move = True
        self.__game_over = False

        self.safe_tiles_left = 0

        self.tiles = dict()

        self.__queue = set()

        self.__columns = 0
        self.__rows = 0
        self.__mines = 0

        self.mines_left = tkinter.IntVar()
        self.count = tkinter.Label(self)
        self.mines_left.trace("w",
                              lambda *args: self.count.config(text="Мин осталось: {}".format(self.mines_left.get())))
        self.mines_left.set(self.__mines)

        self.timer = timer.Timer(self, lambda n: "Время: {}".format(int(n)))

        self.custom  = Custom(self)

        self.menu = tkinter.Menu(master, tearoff=False)
        self.menu.add_command(label="Новая игра", command=self.new_game)
        self.menu.add_command(label="Заново", command=self.reset_board)
        self.menu.add_separator()
        self.menu.add_command(label="Легко", command=lambda: self.set_dimensions(*Minesweeper.EASY))
        self.menu.add_command(label="Средне", command=lambda: self.set_dimensions(*Minesweeper.MEDIUM))
        self.menu.add_command(label="Сложно", command=lambda: self.set_dimensions(*Minesweeper.HARD))
        self.menu.add_command(label="Настройки", command=lambda: self.custom.grid())
        self.menu.add_separator()
        self.menu.add_command(label="Выход", command=self.quit)

        self.menu.invoke(3)

        self.grid()

    def reset_board(self):
        """reset tiles in place"""
        if self.safe_tiles_left == 0:
            tkinter.messagebox.showwarning("Вы уже выиграли!", "Вы не можете перезапустить эту игру.")
            return

        self.pre_game_setup()

        for tile in self.tiles.values():
            tile.reset()

    def new_game(self):
        """
        Sets up a completely new game
        """
        for tile in self.tiles.values():
            tile.destroy()
        self.tiles.clear()

        self.pre_game_setup()

        self.__first_move = True

        self.place_mines()

    def pre_game_setup(self):
        """
        for steps common to reset() and new_game()
        """
        self.safe_tiles_left = 0
        self.__game_over = False
        self.mines_left.set(self.mines)
        self.timer.stop()
        self.timer.reset()

        if self.custom.grid_info():
            self.custom.grid_remove()
            self.grid()

    def set_dimensions(self, columns, rows, mines):
        if columns in Minesweeper.COLUMNS:
            self.__columns = columns

            self.timer.grid(column=columns-Minesweeper.TIMER_WIDTH, columnspan=Minesweeper.TIMER_WIDTH)
        else:
            raise DimensionError("Невозможно установить столбцы как "+str(columns))

        if rows in Minesweeper.ROWS:
            self.__rows = rows
            self.count.grid(row=rows, columnspan=Minesweeper.COUNT_WIDTH)
            self.timer.grid(row=rows)
        else:
            raise DimensionError("Невозможно установить строки как "+str(rows))

        if mines < Minesweeper.MIN_MINES:
            raise DimensionError("Недостаточно мин.")
        else:
            max_mines = Minesweeper.max_mines(self.columns, self.rows)
            if max_mines < mines:
                raise MineOverflow(max_mines)

            self.__mines = mines
            self.mines_left.set(self.mines)

        self.new_game()

    @property
    def columns(self):
        return self.__columns

    @property
    def rows(self):
        return self.__rows

    @property
    def mines(self):
        return self.__mines

    def set_game_over(self):
        self.timer.stop()
        self.__game_over = True

    @property
    def game_over(self):
        return self.__game_over

    def clear_first_move(self):
        self.__first_move = False

    @property
    def first_move(self):
        return self.__first_move

    def count_surrounding(self, column, row):
        counter = 0
        for n in self.neighbors(column, row):
            if type(self.tiles[n]) == Mine:
                counter += 1
        return counter

    def neighbors(self, column, row):
        xs = (x for x in range(column-1, column+2) if x in range(self.columns))
        for x in xs:
            ys = (y for y in range(row-1, row+2) if y in range(self.rows))
            for y in ys:
                yield (x, y)

    def queue_neighbors(self, column, row):
        """Clear every tile surrounding a Safe with a count of 0 one at a time"""

        being_cleared = bool(self.__queue)

        for n in self.neighbors(column, row):
            self.__queue.add(n)

        if not being_cleared:
            while self.__queue:
                item = self.__queue.pop()
                self.tiles[item].invoke()

    def make_safe(self, clicked):
        safe_tiles = filter(lambda x: type(x[1]) == Safe, self.tiles.items())
        other, tile = random.choice(list(safe_tiles))

        self.tiles[clicked], self.tiles[other] = self.tiles[other], self.tiles[clicked]
        self.tiles[clicked].grid(column=clicked[0], row=clicked[1])
        self.tiles[other].grid(column=other[0], row=other[1])

        if tile.flagged:
            tile.flag()
            self.tiles[other].flag()

        self.tiles[other].reset()
        self.tiles[clicked].invoke()

    def place_mines(self):
        indices = [(x, y) for x in range(self.columns) for y in range(self.rows)]

        random.shuffle(indices)
        mine_indices = indices[:self.mines]

        for index in indices:
            if index in mine_indices:
                self.tiles[index] = Mine(self)
            else:
                self.tiles[index] = Safe(self)
            self.tiles[index].grid(column=index[0], row=index[1])

    def explode(self):
        if self.__game_over:
            return

        self.set_game_over()
        for tile in self.tiles.values():
            if type(tile) == Mine:
                tile.invoke()
            else:
                if tile.flagged:
                    tile.flag()
                    tile.config(text="?", disabledforeground="gray")
                tile["state"] = tkinter.DISABLED
        self.play_again_or_quit("Конец игры!", "Вы проиграли.")

    def endgame(self):
        if self.__game_over or self.safe_tiles_left > 0:
            return

        self.set_game_over()

        for m in filter(lambda t: type(t) == Mine and not t.flagged, self.tiles.values()):
            m.mark()

        self.play_again_or_quit("Поздравляю!", "Вы выиграли!")

    def play_again_or_quit(self, title, message):
        if tkinter.messagebox.askquestion(title, message+"Сыграем снова?") == tkinter.messagebox.YES:
            self.new_game()


class Flaggable(tkinter.Button):
    """
    Superclass of Safe and Mine, handles construction, flagging, and most of reveal().
    """
    HEIGHT = 1
    WIDTH = 2*HEIGHT
    ACTIVE_BACKGROUND = "#" + "e0"*6
    DISABLED_BACKGROUND = '#'+'c'*12
    FLAG_COLOR = "#B82828"
    DEFAULT_DISABLED_FOREGROUND = "#737A6F"

    def __init__(self, master):
        super().__init__(master, command=self.reveal, height=Flaggable.HEIGHT, width=Flaggable.WIDTH, bd=2,
                         bg=Flaggable.ACTIVE_BACKGROUND, disabledforeground=Flaggable.DEFAULT_DISABLED_FOREGROUND)
        self.bind("<Button-3>", lambda e: self.flag())
        self.__flagged = False

    @property
    def flagged(self):
        return self.__flagged

    def flag(self):
        self.master.timer.start()

        if tkinter.DISABLED == self["state"] and not self.flagged:
            return

        self.__flagged = not self.flagged

        if self.flagged:
            self.config(text='М', disabledforeground=Flaggable.FLAG_COLOR, state=tkinter.DISABLED)
            self.master.mines_left.set(self.master.mines_left.get()-1)
        else:
            self.config(text='', fg="gray", state=tkinter.NORMAL)
            self.master.mines_left.set(self.master.mines_left.get()+1)

    def reveal(self):
        self.config(state=tkinter.DISABLED, bg=Flaggable.DISABLED_BACKGROUND, relief=tkinter.SUNKEN)
        self._reveal()

    def reset(self):
        if self.flagged:
            self.flag()
        self.config(text="", state=tkinter.NORMAL, bg=Flaggable.ACTIVE_BACKGROUND, relief=tkinter.RAISED,
                    disabledforeground=Flaggable.DEFAULT_DISABLED_FOREGROUND)

    def _reveal(self):
        raise NotImplementedError("_reveal() is not implemented!")


class Mine(Flaggable):
    BLAST_COLOR = "#FF4000"

    def _reveal(self):
        if self.master.first_move:
            self.master.timer.start()
            location = (self.grid_info()['column'], self.grid_info()['row'])
            self.master.make_safe(location)
            self.master.clear_first_move()

        else:
            self.config(text='X', disabledforeground=Mine.BLAST_COLOR)
            self.master.explode()

    def mark(self):
        self.config(state=tkinter.DISABLED, text="M", disabledforeground=Flaggable.DEFAULT_DISABLED_FOREGROUND)


class Safe(Flaggable):

    COLORS = (None, "#0004FF", "#0F9111", "#000000", "#5b076b", "#999349", "#100076", "#6467CC", "#017615")

    def __init__(self, master):
        super().__init__(master)
        self.master.safe_tiles_left += 1

    def _reveal(self):
        self.master.timer.start()
        self.master.safe_tiles_left -= 1
        self.master.clear_first_move()

        info = self.grid_info()
        column = info["column"]
        row = info["row"]
        count = self.master.count_surrounding(column, row)

        if 0 != count:
            self.config(text=str(count), disabledforeground=Safe.COLORS[count])
        else:
            self.master.queue_neighbors(column, row)

        if 0 == self.master.safe_tiles_left:
            self.master.endgame()

    def reset(self):
        self.master.safe_tiles_left += 1
        super().reset()


class Custom(tkinter.Frame):
    """Manually sets dimensions for minesweeper"""
    def __init__(self, game, **options):
        super().__init__(game.master, **options)
        self.game = game

        tkinter.Frame(self, bd=1, height=120, width=2, relief=tkinter.SUNKEN)\
            .grid(column=2, rowspan=3, padx=7, pady=7)

        ENTRY_COLUMN = 3
        ENTRY_WIDTH = 5

        row = 0

        class SetDim(tkinter.Entry):
            def __init__(self, master, dim_name, min, max):
                nonlocal row

                def valid(new_string):
                    return new_string == "" or new_string.isdigit()

                tkinter.Label(master, text="{}:\n({}-{})".format(dim_name, min, max)).grid(row=row)

                super().__init__(master, width=ENTRY_WIDTH,
                                 validate='key', vcmd=(master.register(valid), '%P'))
                self.grid(row=row, column=ENTRY_COLUMN)
                row += 1

            def get(self):
                return int(super().get())

            def insert(self, index, string):
                # clear first
                self.delete(0, tkinter.END)
                super().insert(index, string)

        def minimum(r):
            return r.start

        def maximum(r):
            return r.stop-r.step

        MIN_COL, MAX_COL = minimum(Minesweeper.COLUMNS), maximum(Minesweeper.COLUMNS)
        MIN_ROWS, MAX_ROWS = minimum(Minesweeper.ROWS), maximum(Minesweeper.ROWS)
        MIN_MINES, MAX_MINES = Minesweeper.MIN_MINES, Minesweeper.max_mines(MAX_COL, MAX_ROWS)


        self.columns = SetDim(self, "Колонок", MIN_COL, MAX_COL)
        self.rows = SetDim(self, "Строк", MIN_ROWS, MAX_ROWS)
        self.mines = SetDim(self, "Мин", MIN_MINES, MAX_MINES)

        def cancel():
            self.grid_remove()
            game.grid()
        tkinter.Button(self, text="Отмена", command=cancel).grid(row=row, column=ENTRY_COLUMN)


        def ok():
            try:
                game.set_dimensions(self.columns.get(), self.rows.get(), self.mines.get())
            except ValueError:
                tkinter.messagebox.showerror(message="Вы должны заполнить все записи.")

            except MineOverflow as mo:
                self.mines.insert(0, str(mo.maximum))
                tkinter.messagebox.showwarning(message=mo.message)

            except DimensionError as de:
                tkinter.messagebox.showwarning(message=de.message)
            else:
                self.grid_remove()
                game.grid()

        tkinter.Button(self, text="ОК", command=ok).grid(row=row)

    def grid(self, **options):
        self.game.grid_remove()
        super().grid(**options)
        self.columns.insert(0,str(self.game.columns))
        self.rows.insert(0, str(self.game.rows))
        self.mines.insert(0, str(self.game.mines))

class MinesweeperException(Exception):
    pass

class DimensionError(MinesweeperException):
    def __init__(self, message):
        self.message = message

class MineOverflow(DimensionError):
    def __init__(self, mines):
        super().__init__("You can only have up to {} mines for this board size!".format(mines))
        self.maximum = mines

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Практика 4")
    root.resizable(False, False)
    minesweeper = Minesweeper(root)

    top = tkinter.Menu(root)
    top.add_cascade(label="Игра", menu=minesweeper.menu)
    root.config(menu=top)

    root.mainloop()