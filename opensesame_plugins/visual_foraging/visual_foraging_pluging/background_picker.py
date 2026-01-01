from qtpy import QtCore, QtWidgets, QtGui
import json
from libqtopensesame.widgets.pool_widget import select_from_pool


class BackgroundPicker(QtWidgets.QWidget):
    textChanged = QtCore.Signal(str)

    def __init__(self, parent=None, main_window=None, plugin=None):
        super().__init__(parent)
        self.main_window = main_window
        self._data = None  # {"type": "color"|"image", "value": "..."} or None

        # UI --------------------------------------------------------------
        self.label = QtWidgets.QLabel("Background:")
        self.edit = QtWidgets.QLineEdit()
        self.edit.setReadOnly(True)
        self.btn = QtWidgets.QPushButton("…")
        self.btn.setFixedWidth(32)

        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)
        h.addWidget(self.label)
        h.addWidget(self.edit)
        h.addWidget(self.btn)

        self.btn.clicked.connect(self.open_dialog)

    # ------------------------------------------------------------------
    # Dialog
    # ------------------------------------------------------------------

    def open_dialog(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Select background")

        layout = QtWidgets.QVBoxLayout(dlg)

        # --- COLOR ROW ---------------------------------------------------
        color_row = QtWidgets.QHBoxLayout()
        color_lbl = QtWidgets.QLabel("Background color:")
        color_btn = QtWidgets.QPushButton("Choose…")

        color_row.addWidget(color_lbl)
        color_row.addWidget(color_btn)
        color_row.addStretch()
        layout.addLayout(color_row)

        def choose_color():
            col = QtWidgets.QColorDialog.getColor(parent=self)
            if col.isValid():
                self._data = {
                    "type": "color",
                    "value": col.name()
                }
                self.update_display()

        color_btn.clicked.connect(choose_color)

        # --- IMAGE ROW ---------------------------------------------------
        img_row = QtWidgets.QHBoxLayout()
        img_lbl = QtWidgets.QLabel("Background image:")
        img_btn = QtWidgets.QPushButton("Choose…")

        img_row.addWidget(img_lbl)
        img_row.addWidget(img_btn)
        img_row.addStretch()
        layout.addLayout(img_row)

        def choose_image():
            fname = select_from_pool(self.main_window, parent=self)
            if fname:
                self._data = {
                    "type": "image",
                    "value": fname
                }
                self.update_display()


        img_btn.clicked.connect(choose_image)
        img_btn.clicked.connect(self.plugin.apply_edit_changes)

        # --- CLEAR ROW ---------------------------------------------------
        clear_row = QtWidgets.QHBoxLayout()
        clear_lbl = QtWidgets.QLabel("Clear:")
        clear_btn = QtWidgets.QPushButton("Reset")

        clear_row.addWidget(clear_lbl)
        clear_row.addWidget(clear_btn)
        clear_row.addStretch()
        layout.addLayout(clear_row)

        def clear():
            self._data = None
            self.update_display()

        clear_btn.clicked.connect(clear)

        # --- OK / CANCEL -------------------------------------------------
        bbox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel
        )
        layout.addWidget(bbox)
        bbox.accepted.connect(dlg.accept)
        bbox.accepted.connect(self.plugin.apply_edit_changes)
        bbox.rejected.connect(dlg.reject)

        dlg.exec_()

    # ------------------------------------------------------------------
    # Display + serialization
    # ------------------------------------------------------------------

    def update_display(self):
        if self._data is None:
            self.edit.setText("")
        elif self._data["type"] == "color":
            self.edit.setText(f"color: {self._data['value']}")
        else:
            self.edit.setText(f"image: {self._data['value']}")

        self.textChanged.emit(self.text())

    def text(self):
        return json.dumps(self._data) if self._data else ""

    def setText(self, text):
        try:
            self._data = json.loads(text)
        except:
            self._data = None
        self.update_display()

