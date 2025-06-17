"""Dialog to configure a parameter for plotting."""

from __future__ import annotations

from PyQt5 import QtWidgets, QtGui


class ParamDialog(QtWidgets.QDialog):
    def __init__(self, fields: list[str], parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Параметр")
        self.setModal(True)

        self.field_box = QtWidgets.QComboBox()
        self.field_box.addItems(fields)

        self.name_edit = QtWidgets.QLineEdit()
        self.units_box = QtWidgets.QComboBox()
        self.view_box = QtWidgets.QComboBox()
        self.view_box.addItems(["График", "Текст"])
        self.color_btn = QtWidgets.QPushButton("Цвет")
        self.fill_box = QtWidgets.QComboBox()
        self.palette_box = QtWidgets.QComboBox()
        self.palette_box.addItems(["1", "2", "3"])
        self.ok_btn = QtWidgets.QPushButton("OK")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        self.color = QtGui.QColor("#ff0000")
        self.color_btn.clicked.connect(self.choose_color)

        form = QtWidgets.QFormLayout()
        form.addRow("Поле", self.field_box)
        form.addRow("Имя", self.name_edit)
        form.addRow("Ед.", self.units_box)
        form.addRow("Вид", self.view_box)
        form.addRow(self.color_btn)
        form.addRow("Палетка", self.palette_box)

        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(self.ok_btn)
        buttons.addWidget(self.cancel_btn)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def choose_color(self) -> None:
        color = QtWidgets.QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color

    def get_config(self) -> dict[str, object]:
        return {
            "field": self.field_box.currentText(),
            "name": self.name_edit.text() or self.field_box.currentText(),
            "units": self.units_box.currentText(),
            "view": self.view_box.currentText(),
            "color": self.color,
            "palette": int(self.palette_box.currentText()) - 1,
        }

