#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
from typing import Union, Optional, TypedDict
from dataclasses import dataclass, field
from PIL import Image as Image_mod
from PIL import ImageTk
import geometry as G
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

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        print(f'Set {self.name}.visible to {value}')
        self._visible = value
    

class Lifts(dict[str, Lift]):
    def add(self, lift_name: str, image_dir: str | None = None) -> Lift:
        if image_dir is None:
            image_dir = os.path.expanduser('~/Downloads/')
        if lift_name not in self:
            image = Image_mod.open(os.path.join(
                image_dir,
                f"{lift_name.replace(' ', '_')}.jpg")).resize(G.IMAGE)
            photo = ImageTk.PhotoImage(image)
            saved_photos.append(photo)
            self[lift_name] = Lift(lift_name, photo)
            self[lift_name].visible = True
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
