# -*- coding: utf-8 -*-
#
# Copyright © 2009- The Spyder Development Team
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)

"""
Provides QtSvg classes and functions.
"""

import os

from . import QT_API
from . import PYQT5_API
from . import PYQT4_API
from . import PYSIDE_API
from . import PythonQtError


if os.environ[QT_API] in PYQT5_API:
    from PyQt5.QtSvg import *
elif os.environ[QT_API] in PYQT4_API:
    from PyQt4.QtSvg import *
elif os.environ[QT_API] in PYSIDE_API:
    from PySide.QtSvg import *
else:
    raise PythonQtError('No Qt bindings could be found')
