from qtpy import QtCore, QtWidgets, QtGui
import json
from libqtopensesame.widgets.pool_widget import select_from_pool
from .serialization_helpers import serialize_elements, deserialize_elements


class BackgroundSelector(QtWidgets.QWidget):
    textChanged = QtCore.Signal(str)

    def __init__(self, parent=None, main_window=None, plugin=None):
        super().__init__(parent)
        self.main_window = main_window
        self.plugin = plugin

        # Store BOTH values
        self._data = {
            "color": None,
            "image": None
        }

        # ------------------------------------------------------------------
        # UI ELEMENTS
        # ------------------------------------------------------------------

        # --- Color ---
        self.color_label = QtWidgets.QLabel("Background color:")

        self.color_preview = QtWidgets.QLabel()
        self.color_preview.setFixedSize(24, 24)
        self.color_preview.setStyleSheet("background: none; border: 1px solid #aaa;")

        self.color_btn = QtWidgets.QPushButton("…")
        self.color_btn.setFixedWidth(32)

        # --- Image ---
        self.image_label = QtWidgets.QLabel("Background image:")

        self.image_edit = QtWidgets.QLineEdit()
        self.image_edit.setReadOnly(True)
        self.image_edit.setFixedWidth(140)   # smaller field as requested

        self.image_btn = QtWidgets.QPushButton("…")
        self.image_btn.setFixedWidth(32)

        self.image_clear_btn = QtWidgets.QPushButton("×")
        self.image_clear_btn.setFixedWidth(24)

        # ------------------------------------------------------------------
        # LAYOUT (single row)
        # ------------------------------------------------------------------

        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)

        # LEFT: color
        h.addWidget(self.color_label)
        h.addWidget(self.color_preview)
        h.addWidget(self.color_btn)

        h.addSpacing(20)

        # RIGHT: image
        h.addWidget(self.image_label)
        h.addWidget(self.image_edit)
        h.addWidget(self.image_btn)
        h.addWidget(self.image_clear_btn)

        h.addStretch()

        # Connect events
        self.color_btn.clicked.connect(self.pick_color)
        self.image_btn.clicked.connect(self.pick_image)
        self.image_clear_btn.clicked.connect(self.clear_image)

    # ------------------------------------------------------------------
    # Picking actions
    # ------------------------------------------------------------------

    def pick_color(self):
        col = QtWidgets.QColorDialog.getColor(parent=self)
        if col.isValid():
            self._data["color"] = col.name()
            self.update_display()
            if self.plugin:
                self.plugin.apply_edit_changes()

    def pick_image(self):
        fname = select_from_pool(self.main_window, parent=self)
        if fname:
            self._data["image"] = fname
            self.update_display()
            if self.plugin:
                self.plugin.apply_edit_changes()

    def clear_image(self):
        self._data["image"] = None
        self.update_display()
        if self.plugin:
            self.plugin.apply_edit_changes()

    # ------------------------------------------------------------------
    # Update UI
    # ------------------------------------------------------------------

    def update_display(self):
        # Color preview
        if self._data["color"]:
            self.color_preview.setStyleSheet(
                f"background: {self._data['color']}; border: 1px solid #000;"
            )
        else:
            self.color_preview.setStyleSheet(
                "background: none; border: 1px solid #aaa;"
            )

        # Image filename
        self.image_edit.setText(self._data["image"] or "")

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def text(self):
        # return empty string if both are None
        # if not self._data["color"] and not self._data["image"]:
        #   return '<"color": "#000000"; "image": "">'
        #return json.dumps(self._data)
        return serialize_elements(self._data)

    def setText(self, text):
        try:
            #data = json.loads(text)
            data = deserialize_elements(text)
            self._data = {
                "color": data.get("color"),
                "image": data.get("image")
            }
        except:
            self._data = {"color": None, "image": None}

        self.update_display()

