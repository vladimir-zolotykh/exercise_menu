#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import NamedTuple


class Size(NamedTuple):
    width: int = 0
    height: int = 0


IMAGE = Size(90, 160)
BORDER = Size(2, 2)
ROW_HEIGHT = IMAGE[0] + 2 * BORDER[1]
TEXT_WIDTH = 200                # 10 pix / char

