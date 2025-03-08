#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
# from collections import namedtuple
from types import MethodType
from dataclasses import dataclass, field
from typing import Optional, Any, cast, Callable, Union, Generator
import copy
import tkinter as tk
from tkinter import font as tkfont
from tkinter.messagebox import askokcancel, showwarning
from PIL import Image as Image_mod
from PIL import ImageTk
from scrolledcanvas import ScrolledCanvas
import geometry as G
# import exerdir as ED
import lifts as ED

# saved_photos = []
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
        self._row: int = 0      # canvas row (0-based)
        self._x: int = 0
        self._y: int = 0

    def _get_xy(self, row: int) -> tuple[int, int]:
        return 0 + G.BORDER.width, row * G.ROW_HEIGHT + G.BORDER.height


    def add_to_canvas(
            self, *, image: ImageTk.PhotoImage, name: str
    ) -> tuple[int, int, int]:
        x0, y0 = self._get_xy(self._row)
        image_id = self.create_image(x0, y0, image=image, anchor=tk.NW)
        x1 = x0 + G.BORDER[0] + G.IMAGE[0] + G.BORDER[0]
        name_id = self.create_text(x1, y0, text=name, anchor=tk.NW)
        self._row += 1
        return self._row - 1, image_id, name_id


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
        self.selected_exer: Optional[ED.Lift] = None
        self.exercises = ED.Lifts({})
        assert menu
        self.menu = menu
        self.add_menu = add_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Add', menu=add_menu)
        self.del_menu = del_menu = tk.Menu(menu, name='del_menu', tearoff=0)
        menu.add_cascade(label='Del', menu=del_menu)
        self.initialize_exercises()
        self.update_menu()
        self.configure(scrollregion = self.bbox("all"))
        self.bind("<Button-1>", self.on_click)

    def initialize_exercises(self):
        for name, img in dirx.items():
            self.exercises.add(name)
        self.refresh()

    def update_menu(self) -> None:
        def callback(
                meth: Callable[[str], None], name: str
        ) -> Callable[[], None]:
            def _call_method():
                meth(name)
            return _call_method

        self.add_menu.delete(0, tk.END)
        self.del_menu.delete(0, tk.END)
        for name, lift in self.exercises.items():
            if lift.visible:
                self.del_menu.add_command(
                    label=name, command=callback(self.hide_lift, name))
            else:
                self.add_menu.add_command(
                    label=name, command=callback(self.show_lift, name))

    def highlight_rect(
            self, exer_row: ED.Lift, fill: Optional[str] = None
    ) -> None:
        """highlight_rect(EX_ROW, fill='lightblue') - to highlight,
        highlight_rect(EX) - undo highlight"""
        if fill is None and isinstance(ED.select_rect.line_id, int):
            line_id = ED.select_rect.line_id
            ED.select_rect.line_id = None
            self.delete(line_id)
            return
        row = exer_row.row
        assert isinstance(row, int)
        x0, y0 = self._get_xy(row)
        x1 = (x0 + G.BORDER.width + G.IMAGE.width + G.BORDER.width +
              G.TEXT_WIDTH)
        y1 = y0 + G.BORDER.height + G.IMAGE.height
        coord = list(map(float, (x0, y0, x1, y0, x1, y1, x0, y1)))
        ED.select_rect = ED.SelectRect(
            coord=coord, fill=fill,
            line_id=self.create_line(*coord, width=2, fill=cast(str, fill)))

    def on_click(self, event: tk.Event):
        item = self.find_closest(self.canvasx(event.x), self.canvasy(event.y))
        typ: str = cast(str, self.type(item[0]))
        if typ == 'line':       # ignore the border
            return
        if self.selected_exer:  # undo selected rect
            self.highlight_rect(self.selected_exer)
        ex: ED.Lift | None
        kw: ED.FindArgs = {}
        if typ == 'image':
            kw['image_id'] = item[0]
        elif typ == 'text':
            kw['name_id'] = item[0]
        else:
            raise TypeError(f'{typ}: Invalid item type '
                            f'(must be "image" or "text")')
        if (ex := self.exercises.find(**kw)):
            self.selected_exer = ex
            self.highlight_rect(ex, fill='lightblue')

    def hide_lift(self, exer_name: Optional[str] = None) -> None:
        """Remove EXER_NAME from canvas"""

        ex: ED.Lift | None
        if exer_name:
            ex = self.exercises.find(name=exer_name)
        elif self.selected_exer:
            ex = self.selected_exer
        else:
            showwarning(f'{__name__}.showwarning',
                    f'Select exercise to delete', parent=self)
            return
        assert ex
        if askokcancel(f'{__name__}.askokcancel',
                       f'Delete exercise {ex.name}? ', parent=self):
            ex.visible = False
            self.update_menu()
            self.refresh()

    def refresh(self) -> None:
        self.delete('all')
        super()._rewind()
        for name, lift in self.exercises.items():
            if lift.visible:
                im: ImageTk.PhotoImage = lift.image
                row, image_id, name_id = self.add_to_canvas(
                    image=im, name=lift.name)
                lift.row = row
                lift.image_id, lift.name_id = image_id, name_id
        self.configure(scrollregion = self.bbox("all"))

    def show_lift(self, name: str) -> None:
        lift = self.exercises.find(name=name)
        assert lift
        lift.visible = True
        self.update_menu()
        self.refresh()

class RegisterFrame(tk.Frame):
    def __init__(self, owner, *, menu):
        super().__init__(owner)
        canvas = RegisterCash(self, menu=menu)
        canvas.grid(column=0, row=0, sticky=tk.NSEW)
 
