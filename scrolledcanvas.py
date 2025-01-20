#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


class ScrolledCanvas(tk.Canvas):
    def __init__(self, owner, **kwargs):
        super().__init__(owner, **kwargs)
