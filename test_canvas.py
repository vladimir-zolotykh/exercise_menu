#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from PIL import Image, ImageTk
from scrolledcanvas import grid_expand
from register import RegisterFrame


if __name__ == '__main__':
    root = tk.Tk()
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label='Delete exercise', command=None)
    menu.add_command(label='Add exercise', command=None)
    root['menu'] = menu
    grid_expand(root)
    frame = RegisterFrame(root)
    frame.grid(column=0, row=0, sticky=tk.NSEW)
    grid_expand(frame)
    tk.mainloop()
