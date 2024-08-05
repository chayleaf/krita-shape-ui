from PyQt5.QtCore import QPoint, QRectF
from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
)
from krita import *


class KritaShapeUIDocker(DockWidget):

    def __init__(self):
        super().__init__()
        self.inst = Krita.instance()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setWindowTitle(i18n("Shape UI"))
        self.shape = QComboBox()
        self.shape.addItems([i18n("Line"), i18n("Ellipse"), i18n("Rectangle")])
        l1 = QHBoxLayout()
        l2 = QHBoxLayout()
        l3 = QHBoxLayout()
        l4 = QHBoxLayout()
        l5 = QHBoxLayout()
        layout.addLayout(l1)
        layout.addLayout(l2)
        layout.addLayout(l3)
        layout.addLayout(l4)
        layout.addLayout(l5)
        self.x1 = self.coord_box()
        self.y1 = self.coord_box()
        l1.addWidget(self.x1)
        l1.addWidget(self.y1)
        self.x2 = self.coord_box()
        self.y2 = self.coord_box()
        l2.addWidget(self.x2)
        l2.addWidget(self.y2)
        self.p1 = self.pressure_box()
        self.p2 = self.pressure_box()
        l3.addWidget(self.p1)
        l3.addWidget(self.p2)
        flipX = QPushButton(i18n("Flip X"))
        flipY = QPushButton(i18n("Flip Y"))
        drawBtn = QPushButton(i18n("Draw"))
        selBtn = QPushButton(i18n("Use Selection"))
        l5.addWidget(self.shape)
        l5.addWidget(drawBtn)
        l4.addWidget(flipX)
        l4.addWidget(flipY)
        l4.addWidget(selBtn)
        flipX.released.connect(self.slot_flip_x)
        flipY.released.connect(self.slot_flip_y)
        drawBtn.released.connect(self.slot_draw)
        selBtn.released.connect(self.slot_use_selection)
        self.setWidget(widget)

    def slot_draw(self):
        doc = self.inst.activeDocument()
        node = doc.activeNode()
        x1, y1, x2, y2 = self.get_coords()
        shape = self.shape.currentIndex()
        if shape == 0:
            node.paintLine(
                QPoint(x1, y1), QPoint(x2, y2), self.p1.value(), self.p2.value()
            )
        elif shape == 1:
            node.paintEllipse(QRectF(x1, y1, x2 - x1, y2 - y1))
        elif shape == 2:
            node.paintRectangle(QRectF(x1, y1, x2 - x1, y2 - y1))

    def get_coords(self) -> tuple[int, int, int, int]:
        return (
            self.x1.value(),
            self.y1.value(),
            self.x2.value(),
            self.y2.value(),
        )

    def set_coords(self, x1: int, y1: int, x2: int, y2: int):
        self.x1.setValue(x1)
        self.x2.setValue(x2)
        self.y1.setValue(y1)
        self.y2.setValue(y2)

    def slot_flip_x(self):
        x1, y1, x2, y2 = self.get_coords()
        self.set_coords(x2, y1, x1, y2)

    def slot_flip_y(self):
        x1, y1, x2, y2 = self.get_coords()
        self.set_coords(x1, y2, x2, y1)

    def slot_use_selection(self):
        doc = self.inst.activeDocument()
        sel = doc.selection()
        self.set_coords(sel.x(), sel.y(), sel.x() + sel.width(), sel.y() + sel.height())

    def coord_box(self) -> QSpinBox:
        ret = QSpinBox()
        ret.setSingleStep(1)
        ret.setMinimum(-99999)
        ret.setMaximum(99999)
        return ret

    def pressure_box(self) -> QDoubleSpinBox:
        ret = QDoubleSpinBox()
        ret.setSingleStep(0.01)
        ret.setMaximum(1.0)
        ret.setMinimum(0.0)
        ret.setValue(1.0)
        return ret

    def canvasChanged(self, canvas):
        pass
