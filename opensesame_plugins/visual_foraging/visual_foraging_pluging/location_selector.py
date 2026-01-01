from qtpy import QtCore, QtWidgets

class LocationSelector(QtWidgets.QWidget):
    textChanged = QtCore.Signal(str)

    def __init__(self, plugin, parent=None):
        """
        plugin: reference to OpenSesame plugin
        """
        super().__init__(parent)
        self.plugin = plugin

        # --- Main layout ---
        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)

        # Label
        lbl = QtWidgets.QLabel("Locations:")
        h.addWidget(lbl)

        # Mode combo
        self.mode_combo = QtWidgets.QComboBox()
        self.mode_combo.addItems(["grid", "scatter"])
        self.mode_combo.editTextChanged.connect(self.plugin.apply_edit_changes)
        h.addWidget(self.mode_combo)

        # Option area (dynamic)
        self.option_widget = QtWidgets.QWidget()
        self.option_layout = QtWidgets.QHBoxLayout(self.option_widget)
        self.option_layout.setContentsMargins(0, 0, 0, 0)
        h.addWidget(self.option_widget)
        h.addStretch()

        # --- Scatter controls ---
        self.scatter_mean_x = QtWidgets.QDoubleSpinBox()
        self.scatter_mean_x.setRange(-10000, 10000)
        self.scatter_mean_x.setValue(0)
        self.scatter_std_x = QtWidgets.QDoubleSpinBox()
        self.scatter_std_x.setRange(0, 10000)
        self.scatter_std_x.setValue(50)

        self.scatter_mean_y = QtWidgets.QDoubleSpinBox()
        self.scatter_mean_y.setRange(-10000, 10000)
        self.scatter_mean_y.setValue(0)
        self.scatter_std_y = QtWidgets.QDoubleSpinBox()
        self.scatter_std_y.setRange(0, 10000)
        self.scatter_std_y.setValue(50)

        # --- Grid controls (integer only) ---
        self.grid_rows = QtWidgets.QSpinBox()
        self.grid_rows.setRange(1, 1000)
        self.grid_rows.setValue(7)

        self.grid_cols = QtWidgets.QSpinBox()
        self.grid_cols.setRange(1, 1000)
        self.grid_cols.setValue(12)

        self.grid_jitter_x = QtWidgets.QSpinBox()
        self.grid_jitter_x.setRange(0, 1000)
        self.grid_jitter_x.setValue(20)

        self.grid_jitter_y = QtWidgets.QSpinBox()
        self.grid_jitter_y.setRange(0, 1000)
        self.grid_jitter_y.setValue(20)

        self.grid_spacing_x = QtWidgets.QSpinBox()
        self.grid_spacing_x.setRange(1, 10000)
        self.grid_spacing_x.setValue(120)

        self.grid_spacing_y = QtWidgets.QSpinBox()
        self.grid_spacing_y.setRange(1, 10000)
        self.grid_spacing_y.setValue(120)

        # Connect changes to update display & plugin
        widgets_to_connect = [
            self.mode_combo,
            self.scatter_mean_x, self.scatter_std_x, self.scatter_mean_y, self.scatter_std_y,
            self.grid_rows, self.grid_cols,
            self.grid_jitter_x, self.grid_jitter_y,
            self.grid_spacing_x, self.grid_spacing_y
        ]
        for w in widgets_to_connect:
            w.valueChanged.connect(self.update_display) if isinstance(w, QtWidgets.QSpinBox) or isinstance(w, QtWidgets.QDoubleSpinBox) else w.currentIndexChanged.connect(self.update_display)

        self.textChanged.connect(self.plugin.apply_edit_changes)

        # Initialize display
        self.update_display()

    def update_display(self):
        # Clear current option layout
        for i in reversed(range(self.option_layout.count())):
            widget = self.option_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        mode = self.mode_combo.currentText()
        if mode == "grid":
            self.option_layout.addWidget(QtWidgets.QLabel("Rows:"))
            self.option_layout.addWidget(self.grid_rows)
            self.option_layout.addWidget(QtWidgets.QLabel("Cols:"))
            self.option_layout.addWidget(self.grid_cols)
            self.option_layout.addWidget(QtWidgets.QLabel("Jitter X:"))
            self.option_layout.addWidget(self.grid_jitter_x)
            self.option_layout.addWidget(QtWidgets.QLabel("Jitter Y:"))
            self.option_layout.addWidget(self.grid_jitter_y)
            self.option_layout.addWidget(QtWidgets.QLabel("Spacing X:"))
            self.option_layout.addWidget(self.grid_spacing_x)
            self.option_layout.addWidget(QtWidgets.QLabel("Spacing Y:"))
            self.option_layout.addWidget(self.grid_spacing_y)
        else:
            self.option_layout.addWidget(QtWidgets.QLabel("Mean X:"))
            self.option_layout.addWidget(self.scatter_mean_x)
            self.option_layout.addWidget(QtWidgets.QLabel("Std X:"))
            self.option_layout.addWidget(self.scatter_std_x)
            self.option_layout.addWidget(QtWidgets.QLabel("Mean Y:"))
            self.option_layout.addWidget(self.scatter_mean_y)
            self.option_layout.addWidget(QtWidgets.QLabel("Std Y:"))
            self.option_layout.addWidget(self.scatter_std_y)

        self.textChanged.emit(self.text())

    # Serialization for OpenSesame
    def text(self):
        mode = self.mode_combo.currentText()
        if mode == "grid":
            return f"<mode: grid, rows: {self.grid_rows.value()}, cols: {self.grid_cols.value()}, jitter_x: {self.grid_jitter_x.value()}, jitter_y: {self.grid_jitter_y.value()}, spacing_x: {self.grid_spacing_x.value()}, spacing_y: {self.grid_spacing_y.value()}>"
        else:
            return f"<mode: scatter, mean_x: {self.scatter_mean_x.value()}, std_x: {self.scatter_std_x.value()}, mean_y: {self.scatter_mean_y.value()}, std_y: {self.scatter_std_y.value()}>"

    def setText(self, text):
            if text.startswith("<") and text.endswith(">"):
                text = text[1:-1]
                parts = [p.strip() for p in text.split(",")]
                mode_part = parts[0].split(":")[1].strip()
                self.mode_combo.setCurrentText(mode_part)
                if mode_part == "grid":
                    self.grid_rows.setValue(int(parts[1].split(":")[1]))
                    self.grid_cols.setValue(int(parts[2].split(":")[1]))
                    self.grid_jitter_x.setValue(int(parts[3].split(":")[1]))
                    self.grid_jitter_y.setValue(int(parts[4].split(":")[1]))
                    self.grid_spacing_x.setValue(int(parts[5].split(":")[1]))
                    self.grid_spacing_y.setValue(int(parts[6].split(":")[1]))
                else:
                    self.scatter_mean_x.setValue(float(parts[1].split(":")[1]))
                    self.scatter_std_x.setValue(float(parts[2].split(":")[1]))
                    self.scatter_mean_y.setValue(float(parts[3].split(":")[1]))
                    self.scatter_std_y.setValue(float(parts[4].split(":")[1]))
            self.update_display()

