#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from typing import TypedDict, Callable, Optional
from dataclasses import dataclass, field
from itertools import dropwhile
import re
from PIL import Image, ImageTk


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


@dataclass
class ExerCash:
    row: int                    # canvas row for exercise
    name: str                   # 'squat' or 'bench press'
    image: ImageTk.PhotoImage | None = None
    image_id: int | None = None # canvas image id (exer. pic)
    name_id: int | None = None  # canvas text id (exer. name)
    visible_in_canvas: bool = False


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
            if  (m := re.match('(?P<exer_name>.*)( \(\d+\))?', name)):
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
        # del self[self.index(exer_cash)]
        exer_cash.visible_in_canvas = False
