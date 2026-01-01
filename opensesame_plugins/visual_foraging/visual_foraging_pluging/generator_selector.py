from qtpy import QtCore, QtWidgets, QtGui
import json

class GeneratorSelector(QtWidgets.QWidget):
    textChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = {"type": "scatter"}  # default

        # UI
        self.label = QtWidgets.QLabel("Generator:")
        self.edit = QtWidgets.QLineEdit()
        self.edit.setReadOnly(True)
        self.btn = QtWidgets.QPushButton("…")
        self.btn.setFixedWidth(32)
        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(0,0,0,0)
        h.addWidget(self.label)
        h.addWidget(self.edit)
        h.addWidget(self.btn)
        self.btn.clicked.connect(self.open_dialog)

        # Call update_display AFTER text() is defined (should be OK)
        self.update_display()

    # ------------------------
    # Must keep text() for OpenSesame
    # ------------------------
    def text(self):
        return json.dumps(self._data) if self._data else ""

    def setText(self, text):
        try:
            self._data = json.loads(text)
        except:
            self._data = {"type":"scatter"}
        self.update_display()

