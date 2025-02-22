#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
# from collections import namedtuple
from types import MethodType
from dataclasses import dataclass, field
from typing import Optional, Any, cast, Callable, Union
import copy
import tkinter as tk
from tkinter import font as tkfont
from tkinter.messagebox import askokcancel, showwarning
from PIL import Image as Image_mod
from PIL import ImageTk
from scrolledcanvas import ScrolledCanvas
import geometry as G
import exerdir as ED

saved_photos = []
EXER_LIST = ("squat", "bench press", "deadlift", "pullup", "front squat",
             "overhead press","biceps curl", "back plank")
DirX = dict[str, Union[Image_mod.Image, ImageTk.PhotoImage]]
try:
    dirx: DirX = {
        # Revealed type is "PIL.Image.Image"
        name: Image_mod.open(path).resize(G.IMAGE)
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


    def add_to_canvas(
            self, *, image: ImageTk.PhotoImage, name='', exer_id=0
    ) -> tuple[int, int]:
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
        self.selected_exer: Optional[ED.ExerCash] = None
        self.exercises = ED.ExerDir([])
        assert menu
        # if menu:
        self.menu = menu
        self.add_menu = add_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Add', menu=add_menu)
        self.del_menu = del_menu = tk.Menu(menu, tearoff=0)
        self.update_del_menu(del_menu)
        menu.add_cascade(label='Del', menu=del_menu)
        self.initialize_exercises()
        self.update_add_menu(add_menu)
        self.update_del_menu(del_menu)
        self.configure(scrollregion = self.bbox("all"))

        self.bind("<Button-1>", self.on_click)

    def initialize_exercises(self):
        for name, img in dirx.items():
            saved_photos.append(img if isinstance(img, ImageTk.PhotoImage) else
                                ImageTk.PhotoImage(img))
            self.add_to_cashed_exercises(image=saved_photos[-1], name=name)

    def update_add_menu(self, menu: tk.Menu) -> None:
        def make_append(
                name: str, image: ImageTk.PhotoImage
        ) -> Callable[[], None]:
            def _call_method():
                return self.add_to_cashed_exercises(image=image, name=name)
            return _call_method

        n: Optional[int] = menu.index(tk.END)
        if isinstance(n, int):
            # Delete existent entries
            for i in range(n + 1, 1, -1):
                menu.delete(i)
        for exer_cash in self.exercises:
            if not exer_cash.visible:
                if (im := exer_cash.image):
                    menu.add_command(
                        label=exer_cash.name,
                        command=make_append(exer_cash.name, image=im))
                    exer_cash.visible = False

    def update_del_menu(self, menu: tk.Menu) -> None:
        def make_delete_cmd(name: str) -> Callable[[], None]:
            def _call_method():
                self.remove_from_canvas(name)
            return _call_method

        n: Optional[int] = menu.index(tk.END)
        if isinstance(n, int):
            # Delete existent entries
            for i in range(n + 1, 1, -1):
                menu.delete(i)
        for exer_cash in self.exercises:
            if exer_cash.visible:
                menu.add_command(label=exer_cash.name,
                                 command=make_delete_cmd(exer_cash.name))

    def _rewind(self):
        super()._rewind()
        self.exer_i = 0

    def highlight_rect(
            self, exer_row: ED.ExerCash, fill: Optional[str] = None
    ) -> None:
        """highlight_rect(EX_ROW, fill='lightblue') - to highlight,
        highlight_rect(EX) - undo highlight"""
        
        if fill is None and isinstance(ED.select_rect.line_id, int):
            line_id = ED.select_rect.line_id
            ED.select_rect.line_id = None
            self.delete(line_id)
            return
        row = exer_row.row
        x0, y0 = self._get_xy(row)
        x1 = (x0 + G.BORDER.width + G.IMAGE.width + G.BORDER.width +
              G.TEXT_WIDTH)
        y1 = y0 + G.BORDER.height + G.IMAGE.height
        coord = list(map(float, (x0, y0, x1, y0, x1, y1, x0, y1)))
        ED.select_rect.coord = coord
        ED.select_rect.fill = fill
        ED.select_rect.line_id = self.create_line(
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
        ex: ED.ExerCash
        # kw: dict[str, int] = {}
        kw: ED.FindArgs = {}
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
        # if self.menu:
        #     MethodType(_change_label, self.menu)(ex.name)

    def remove_from_canvas(self, exer_name: Optional[str] = None) -> None:
        """Remove EXER_NAME from canvas"""
        
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
            self.exercises.hide_in_exercises(ex)
            self.update_add_menu(self.add_menu)
            self.refresh()

    def refresh(self) -> None:
        self.delete('all')
        # super()._rewind()
        self._rewind()
        exer_dir_copy: list[ED.ExerCash] = copy.copy(self.exercises)
        # for exer_cash in self.exercises:
        self.exercises = ED.ExerDir()
        for exer_cash in exer_dir_copy:
            if exer_cash.visible:
                assert exer_cash.image
                im: ImageTk.PhotoImage = exer_cash.image
                self.add_to_cashed_exercises(image=im, name=exer_cash.name)
        del exer_dir_copy
        self.configure(scrollregion = self.bbox("all"))

    def add_to_cashed_exercises(
            self, *, image: ImageTk.PhotoImage, name: str,
            image_id: Optional[int] = None, name_id: Optional[int] = None
    ):
        if image_id is None or name_id is None:
            image_id, name_id = super().add_to_canvas(
                image=image, name=name, exer_id=self.exer_i)
        self.exercises.append(ED.ExerCash(
            self.exer_i, name, image, image_id, name_id, True))
        self.configure(scrollregion = self.bbox("all"))
        self.exer_i += 1

class RegisterFrame(tk.Frame):
    def __init__(self, owner, *, menu):
        super().__init__(owner)
        canvas = RegisterCash(self, menu=menu)
        canvas.grid(column=0, row=0, sticky=tk.NSEW)
 
