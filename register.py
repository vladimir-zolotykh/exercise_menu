#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
# from collections import namedtuple
from types import MethodType
from dataclasses import dataclass, field
from typing import Optional, Any, Callable, cast, TypedDict
import re
from itertools import dropwhile
import copy
import tkinter as tk
from tkinter import font as tkfont
from tkinter.messagebox import askokcancel, showwarning
from PIL import Image, ImageTk
from scrolledcanvas import ScrolledCanvas
import geometry as G

saved_photos = []
EXER_LIST = ("squat", "bench press", "deadlift", "pullup", "front squat",
             "overhead press","biceps curl", "back plank")
dirx = {}
try:
    dirx = {
        name: Image.open(path).resize(G.IMAGE)
        for name, path in zip(
                EXER_LIST,
                (os.path.expanduser(f'~/Downloads/{xn.replace(" ", "_")}.jpg')
                 for xn in EXER_LIST))
    }
except FileNotFoundError as e:
    print(f'{e.filename}: file not found')
    exit(1)


class Register(ScrolledCanvas):
    def __init__(self, owner: tk.Widget, **kwargs: dict[str, Any]):
        super().__init__(owner, **kwargs)
        self._rewind()

    def _rewind(self) -> None:
        self._row: int = 0
        self._x: int = 0
        self._y: int = 0

    def _get_xy(self, row: Optional[int] = None) -> tuple[int, int]:
        if row is None:
            return self._x, self._y
        else:
            return 0 + G.BORDER.width, row * G.ROW_HEIGHT + G.BORDER.height


    def append(self, *, image=None, name='', exer_id=0) -> tuple[int, int]:
        ex_str = f'{name} ({exer_id})'
        # self.toggle_selection_rect()
        x0, y0 = self._get_xy(self._row)
        image_id = self.create_image(x0, y0, image=image, anchor=tk.NW)
        x1 = x0 + G.BORDER[0] + G.IMAGE[0] + G.BORDER[0]
        name_id = self.create_text(x1, y0, text=ex_str, anchor=tk.NW)

        def font_metrics() -> tuple[int, int]:
            name: str = self.itemcget(name_id, 'font') # 'TkDefaultFont'
            font = tkfont.nametofont(name)
            width = font.measure(ex_str) // len(ex_str)
            height = font.metrics("linespace")
            # font_width = 6, font_height = 17
            return width, height

        font_metrics()
        self._row += 1
        return image_id, name_id


@dataclass
class SelectRect:
    # x0, y0, x1, y1, ...
    coord: list[float] = field(default_factory=list)
    # line_id = canv.create_line()
    line_id: Optional[int] = None
    # 'background', 'lightblue'
    fill: Optional[str] = None


@dataclass
class ExerCash:
    row: int                    # canvas row for exercise
    image: ImageTk.PhotoImage
    name: str                   # 'squat' or 'bench press'
    image_id: int               # canvas image id (exer. pic)
    name_id: int                # canvas text id (exer. name)
    # highlighted rectangle around selected exercise
    select_rect: SelectRect


class FindArgs(TypedDict, total=False):
    name: str
    image_id: int
    name_id: int


class ExerDir(list[ExerCash]):
    def find_exer(
            self, *, name: str = '', image_id: int = 0, name_id: int = 0
    ) -> ExerCash:
        err: TypeError
        predicate: Callable[[ExerCash], bool] = lambda exer: False
        if name:
            requested_name = name
            if  (m := re.match('(?P<exer_name>.*) \(\d+\)', name)):
                requested_name = m.group('exer_name')
                predicate = lambda exer: exer.name != requested_name
            err = TypeError(f'Exercise {requested_name} not found')
        elif image_id or name_id:
            predicate = lambda exer: (exer.image_id != image_id and
                                      exer.name_id != name_id)
            err = TypeError(f'Exercise with ' f'{image_id = } or {name_id = }'
                            f' not found')
        else:
            raise TypeError('Specify name, image_id, or name_id')
        try:
            return next(dropwhile(predicate, self))
        except StopIteration:
            raise err

    def delete_exer(self, exer_cash: ExerCash) -> None:
        """Delete EXER_CASH from self"""
        del self[self.index(exer_cash)]


def _change_label(self, exer_name):
    """Change menu's item LABEL"""

    for item in range(self.index(tk.END) + 1):
        if self.entrycget(item, 'label').startswith('Delete exercise'):
            self.entryconfig(item, label=f'Delete exercise <{exer_name}>')
            return
    raise TypeError('No "Delete exercise" item found')


class RegisterCash(Register):
    def __init__(
            self, owner: tk.Widget, *, menu: tk.Menu, **kwargs: dict[str, Any]
    ):
        super().__init__(owner, **kwargs)
        self.exer_i = 0
        self.selected_exer: Optional[ExerCash] = None
        self.exercises = ExerDir([])
        if menu:
            self.menu = menu
            add_menu = tk.Menu(menu, tearoff=0)
            menu.add_cascade(label='Add', menu=add_menu)
            add_menu.add_command(label='Add exercise', command=lambda: None)
            menu.add_command(label='Delete exercise', command=self.delete_exer)
        self.bind("<Button-1>", self.on_click)

    def _rewind(self):
        super()._rewind()
        self.exer_i = 0

    def highlight_rect(self, exer_row: ExerCash, fill: Optional[str] = None):
        """highlight_rect(EX_ROW, fill='lightblue') - to highlight,
        highlight_rect(EX) - undo highlight"""
        
        if fill is None and isinstance(exer_row.select_rect.line_id, int):
            line_id = exer_row.select_rect.line_id
            exer_row.select_rect.line_id = None
            self.delete(line_id)
            return
        row = exer_row.row
        x0, y0 = self._get_xy(row)
        x1 = (x0 + G.BORDER.width + G.IMAGE.width + G.BORDER.width +
              G.TEXT_WIDTH)
        y1 = y0 + G.BORDER.height + G.IMAGE.height
        coord = list(map(float, (x0, y0, x1, y0, x1, y1, x0, y1)))
        exer_row.select_rect.coord = coord
        exer_row.select_rect.fill = fill
        exer_row.select_rect.line_id = self.create_line(
            *coord, width=2, fill=cast(str, fill))


    def on_click(self, event: tk.Event):
        item = self.find_closest(self.canvasx(event.x), self.canvasy(event.y))
        # self.type(item[0]): 'image', 'text', or 'line'
        typ: str = cast(str, self.type(item[0]))
        if typ == 'line':       # ignore the border
            return
        if self.selected_exer:  # undo selected rect
            # self.draw_rect(row=self.selected_exer.row)
            self.highlight_rect(self.selected_exer)
        ex: ExerCash
        # kw: dict[str, int] = {}
        kw: FindArgs = {}
        if typ == 'image':
            kw['image_id'] = item[0]
        elif typ == 'text':
            kw['name_id'] = item[0]
        else:
            raise TypeError(f'{typ}: Invalid item type '
                            f'(must be "image" or "text")')
        # if (ex := self.exercises.find_exer(image_id=item[0],
        #                                     name_id=item[0])):
        if (ex := self.exercises.find_exer(**kw)):
            self.selected_exer = ex
        # self.draw_rect(row=ex.row, fill='lightblue')
        self.highlight_rect(ex, fill='lightblue')
        if self.menu:
            MethodType(_change_label, self.menu)(ex.name)

    def delete_exer(self, exer_name: Optional[str] = None) -> None:
        """Delete EXER_NAME or .selected_exer exercise"""
        
        if exer_name:
            ex = self.exercises.find_exer(name=exer_name)
        elif self.selected_exer:
            ex = self.selected_exer
        else:
            showwarning(f'{__name__}.showwarning',
                    f'Select exercise to delete', parent=self)
            return
        if askokcancel(f'{__name__}.askokcancel',
                       f'Delete exercise {ex.name}? ', parent=self):
            # self.delete(ex.image_id)
            # self.delete(ex.name_id)
            self.exercises.delete_exer(ex)
            self.refresh()


    def refresh(self) -> None:
        self.delete('all')
        # super()._rewind()
        self._rewind()
        exer_dir_copy: list[ExerCash] = copy.copy(self.exercises)
        # for exer_cash in self.exercises:
        self.exercises = ExerDir()
        for exer_cash in exer_dir_copy:
            self.append(image=exer_cash.image, name=exer_cash.name)
        del exer_dir_copy
        self.configure(scrollregion = self.bbox("all"))
            

    def append(self, *, image=None, name=''):
        image_id, name_id = super().append(
            image=image, name=name, exer_id=self.exer_i)
        self.exercises.append(ExerCash(
            self.exer_i, image, name, image_id, name_id, SelectRect()))
        self.exer_i += 1

class RegisterFrame(tk.Frame):
    def __init__(self, owner, *, menu):
        super().__init__(owner)
        canvas = RegisterCash(self, menu=menu)
        canvas.grid(column=0, row=0, sticky=tk.NSEW)
        for name, img in dirx.items():
            saved_photos.append(ImageTk.PhotoImage(img))
            canvas.append(image=saved_photos[-1], name=name)
        canvas.configure(scrollregion = canvas.bbox("all"))
