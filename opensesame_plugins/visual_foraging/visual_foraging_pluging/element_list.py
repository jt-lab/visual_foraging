"""
Custom multicolumn element list widget for OpenSesame plugins.
"""

import json
import base64
import os
from qtpy import QtCore, QtGui, QtWidgets
from libqtopensesame.widgets.pool_widget import select_from_pool
from .serialization_helpers import serialize_elements, deserialize_elements


class ElementList(QtWidgets.QWidget):
    textChanged = QtCore.Signal(str)
    
   
    COL_ICON = 0
    COL_IMAGE = 1
    COL_TYPE = 2
    COL_ROLE = 3
    COL_VALUE = 4
    COL_SOUND = 5
    COL_ACTION = 6
    COL_RESULT = 7
    COL_AMOUNT = 8

    HEADERS = [
        "", "Image", "Type", "Role", "Value", "Click sound",
        "Click action", "Click Result", "Amount"
    ]
    def __init__(self, parent=None, experiment=None, main_window=None, plugin=None):
        super().__init__(parent)
        self.experiment = experiment
        self.main_window = main_window
        self.plugin = plugin

        # Table --------------------------------------------------------------
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.table.setColumnWidth(self.COL_ICON, 32)
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked |
            QtWidgets.QAbstractItemView.SelectedClicked |
            QtWidgets.QAbstractItemView.EditKeyPressed
        )

        # Buttons -------------------------------------------------------------
        self.add_btn = QtWidgets.QPushButton("+")
        self.add_btn.setFixedWidth(30)

        self.remove_btn = QtWidgets.QPushButton("−")
        self.remove_btn.setFixedWidth(30)

        # Layout --------------------------------------------------------------
        h = QtWidgets.QHBoxLayout()
        h.addWidget(self.table)

        btn_layout = QtWidgets.QVBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addStretch()

        h.addLayout(btn_layout)

        v = QtWidgets.QVBoxLayout(self)
        v.addLayout(h)

    # Signals -------------------------------------------------------------
        self.add_btn.clicked.connect(self.add_item_dialog)
        self.remove_btn.clicked.connect(self.remove_selected_row)

        self.table.itemChanged.connect(self.on_item_changed)
        self.table.itemChanged.connect(plugin.apply_edit_changes)



    # ----------------------------------------------------------------------
    # Serialization
    # ----------------------------------------------------------------------

    def text(self):
        elements = []

        for row in range(self.table.rowCount()):
            element = {
                "image": self._text(row, self.COL_IMAGE),
                "type": self._text(row, self.COL_TYPE),
                "role": self._text(row, self.COL_ROLE),
                "value": int(self._text(row, self.COL_VALUE) or 0),
                "click_sound": self._text(row, self.COL_SOUND),
                "click_action": self._text(row, self.COL_ACTION),
                "click_result": self._text(row, self.COL_RESULT),
               "amount": self._text(row, self.COL_AMOUNT),
            }
            elements.append(element)

        return serialize_elements(elements)



    def setText(self, text):
        self.table.blockSignals(True)
        self.table.setRowCount(0)

        elements = deserialize_elements(text)
        for element in elements:
            self._add_row(element)

        self.table.blockSignals(False)
        self.textChanged.emit(self.text())


    # ----------------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------------

    def _text(self, row, col):
        item = self.table.item(row, col)
        return item.text() if item else ""

    def _add_row(self, d):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Icon item
        icon_item = QtWidgets.QTableWidgetItem()

        image_name = d.get("image")
        if image_name and self.experiment:
            try:
                pix = QtGui.QPixmap(self.experiment.pool[image_name]).scaled(
                    32, 32,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation
                )
                icon_item.setIcon(QtGui.QIcon(pix))
            except Exception:
                pass

        icon_item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table.setItem(row, self.COL_ICON, icon_item)

        # Other columns
        for col, key in [
            (self.COL_IMAGE, "image"),
            (self.COL_TYPE, "type"),
            (self.COL_ROLE, "role"),
            (self.COL_VALUE, "value"),
            (self.COL_SOUND, "click_sound"),
            (self.COL_ACTION, "click_action"),
            (self.COL_RESULT, "click_result"),
            (self.COL_AMOUNT, "amount"),
        ]:
            item = QtWidgets.QTableWidgetItem(str(d.get(key, "")))
            self.table.setItem(row, col, item)
            
        #self.table.resizeColumnsToContents()

            
        

    def on_item_changed(self, item):
        self.textChanged.emit(self.text())
        
    def remove_selected_row(self):
        row = self.table.currentRow()
        if row < 0:
            return  # no selection

        self.table.removeRow(row)
        self.textChanged.emit(self.text())
        self.table.itemChanged.emit(None)


    # ----------------------------------------------------------------------
    # Add-item dialog
    # ----------------------------------------------------------------------

    def add_item_dialog(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Add element")

        form = QtWidgets.QFormLayout(dlg)

        # image
        img_edit = QtWidgets.QLineEdit()
        img_btn = QtWidgets.QPushButton("Select…")

        def choose_image():
            if self.main_window:
                fname = select_from_pool(self.main_window, parent=self)
                if fname:
                    img_edit.setText(fname)
                    # If type field is empty, set it from the filename
                    if not type_edit.text():
                        base = os.path.splitext(os.path.basename(fname))[0] 
                        type_edit.setText(base.replace("_", " "))


        img_btn.clicked.connect(choose_image)
        


        h_img = QtWidgets.QHBoxLayout()
        h_img.addWidget(img_edit)
        h_img.addWidget(img_btn)
        form.addRow("Image:", h_img)

        # type
        type_edit = QtWidgets.QLineEdit()
        form.addRow("Type:", type_edit)

        # role
        role_combo = QtWidgets.QComboBox()
        role_combo.addItems(["target", "distractor"])
        form.addRow("Role:", role_combo)

        # value
        value_spin = QtWidgets.QSpinBox()
        value_spin.setMinimum(0)
        value_spin.setValue(1)
        form.addRow("Value:", value_spin)

        # click sound
        snd_edit = QtWidgets.QLineEdit()
        snd_btn = QtWidgets.QPushButton("Select…")

        def choose_sound():
            if self.main_window:
                fname = select_from_pool(self.main_window, parent=self)
                if fname:
                    snd_edit.setText(fname)


        snd_btn.clicked.connect(choose_sound)

        h_snd = QtWidgets.QHBoxLayout()
        h_snd.addWidget(snd_edit)
        h_snd.addWidget(snd_btn)
        form.addRow("Click sound:", h_snd)

        # click action
        action_combo = QtWidgets.QComboBox()
        action_combo.addItems(["click", "double click", "mouse over"])
        form.addRow("Click action:", action_combo)

        # click result
        result_combo = QtWidgets.QComboBox()
        result_combo.addItems(["vanish", "remain"])
        form.addRow("Click result:", result_combo)
        
        # amount
        amount_spin = QtWidgets.QSpinBox()
        amount_spin.setMinimum(0)
        amount_spin.setValue(1)
        form.addRow("Amount:", amount_spin)

        # Buttons -------------------------------------------------------------
        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel
        )
        form.addRow(btns)

        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)

        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return

        # Collect data
        d = {
            "image": img_edit.text(),
            "type": type_edit.text(),
            "role": role_combo.currentText(),
            "value": value_spin.value(),
            "click_sound": snd_edit.text(),
            "click_action": action_combo.currentText(),
            "click_result": result_combo.currentText(),
            "amount": amount_spin.value(),
        }

        self._add_row(d)
        self.textChanged.emit(self.text())



