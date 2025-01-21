#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from PIL import Image, ImageTk
from scrolledcanvas import ScrolledCanvas
SIZE = (50, 50)


class Register(ScrolledCanvas):
    def __init__(self, owner, **kwargs):
        super().__init__(owner, **kwargs)
        self._x = 0
        self._y = 0

    def append(self, *, image=None, name=''):
        self.create_image(self._x, self._y, image=image, anchor=tk.NW)
        self.create_text(self._x + SIZE[0], self._y, text=name, anchor=tk.NW)
        self._y += SIZE[1]
        
