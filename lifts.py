#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
import os
from typing import Union, Optional, TypedDict
from dataclasses import dataclass, field
from PIL import Image as Image_mod
from PIL import ImageTk
import geometry as G
import register as R
saved_photos: list[ImageTk.PhotoImage] = []

@dataclass
class SelectRect:
    # x0, y0, x1, y1, ...
    coord: list[float] = field(default_factory=list)
    # line_id = canv.create_line()
    line_id: Optional[int] = None
    # 'background', 'lightblue'
    fill: Optional[str] = None

# highlighted rectangle around selected exercise
select_rect: SelectRect = SelectRect()

class FindArgs(TypedDict, total=False):
    name: str
    image_id: int
    name_id: int


@dataclass
class Lift:
    name: str                   # 'squat' or 'bench press'
    image: ImageTk.PhotoImage
    _visible: bool = field(repr=False, init=False, default=False)
    # the attributes below are valid if the LIFT is on the canvas
    row: int | None = None      # canvas row
    image_id: int | None = None
    name_id: int | None = None
    # parent: object = field(repr=False, default=None)
    parent: R.RegisterCash | None = field(repr=False, default=None)
    
    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        if hasattr(self.parent, 'exercises') and value != self._visible:
            assert self.parent
            self._visible = value
            self.parent.update_menu()
            self.parent.refresh()
    

class Lifts(dict[str, Lift]):
    def __init__(
            # self, parent: object, image_dir: str | None = None
            self, parent: R.RegisterCash, image_dir: str | None = None
    ) -> None:
        self.parent = parent
        self.image_dir = (os.path.expanduser('~/Downloads/')
                          if image_dir is None else image_dir)

    def initialize(self, exercise_names: list[str]):
        for name in exercise_names:
            self.add(name)

    def add(self, lift_name: str) -> Lift:
        if lift_name not in self:
            image = Image_mod.open(os.path.join(
                self.image_dir,
                f"{lift_name.replace(' ', '_')}.jpg")).resize(G.IMAGE)
            photo = ImageTk.PhotoImage(image)
            saved_photos.append(photo)
            lift: Lift = Lift(lift_name, photo, parent=self.parent)
            self[lift_name] = lift
            lift.visible = True
        return self[lift_name]

    def find(
            self, *, name: str = '', name_id: int = -1, image_id: int = -1
    ) -> Lift | None:
        k: str
        v: Lift
        for k, v in self.items():
            if name == k or name_id == v.name_id or image_id == v.image_id:
                return v
        return None
