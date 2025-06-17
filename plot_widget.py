"""Custom plot widget for vertical time-depth plots."""

from __future__ import annotations

import pyqtgraph as pg


class TimeDepthAxis(pg.AxisItem):
    """Axis that displays time and depth together."""

    def tickStrings(self, values, scale, spacing):  # type: ignore[override]
        strings = []
        for val in values:
            # assume val represents time in seconds
            depth = ''
            if self.linkedView() is not None:
                depth = f"\n{val}"
            strings.append(f"{val}{depth}")
        return strings


class VerticalPlotWidget(pg.PlotWidget):
    """Plot widget oriented vertically with a TimeDepthAxis."""

    def __init__(self, parent=None):
        super().__init__(parent=parent, axisItems={'left': TimeDepthAxis('left')})
        self.setDownsampling(mode='peak')
        self.setClipToView(True)
        self.invertY(True)
        self.showGrid(x=True, y=True)

