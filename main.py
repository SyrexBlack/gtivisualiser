"""Simple GTI visualiser application."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt5 import QtWidgets
import pyqtgraph as pg

from data_model import DataModel
from param_dialog import ParamDialog
from plot_widget import VerticalPlotWidget


def load_file(model: DataModel, parent: QtWidgets.QWidget) -> None:
    path, _ = QtWidgets.QFileDialog.getOpenFileName(
        parent, "Open Data", str(Path.home()), "Data Files (*.csv *.xls *.xlsx)"
    )
    if not path:
        return
    try:
        model.load(path)
    except Exception as exc:
        QtWidgets.QMessageBox.critical(parent, "Error", str(exc))


def add_parameter(model: DataModel, plots: list[VerticalPlotWidget], parent: QtWidgets.QWidget) -> None:
    if model.data is None:
        QtWidgets.QMessageBox.warning(parent, "No data", "Load data first")
        return
    dialog = ParamDialog(model.data.columns.tolist(), parent)
    if dialog.exec_() != QtWidgets.QDialog.Accepted:
        return
    cfg = dialog.get_config()
    plot = plots[cfg["palette"]]
    x = model.data[cfg["field"]]
    y = model.data["время"]
    plot.plot(x, y, pen=pg.mkPen(color=cfg["color"]))


def main() -> None:
    pg.setConfigOptions(useOpenGL=True)
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("GTI Visualiser")

    model = DataModel()

    central = QtWidgets.QWidget()
    hbox = QtWidgets.QHBoxLayout(central)

    control = QtWidgets.QVBoxLayout()
    load_btn = QtWidgets.QPushButton("Load")
    add_btn = QtWidgets.QPushButton("Add Parameter")
    control.addWidget(load_btn)
    control.addWidget(add_btn)
    control.addStretch()

    plots = [VerticalPlotWidget() for _ in range(3)]
    for p in plots:
        hbox.addWidget(p)

    hbox.addLayout(control, 1)
    window.setCentralWidget(central)

    load_btn.clicked.connect(lambda: load_file(model, window))
    add_btn.clicked.connect(lambda: add_parameter(model, plots, window))

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

