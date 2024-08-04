from krita import DockWidgetFactory, DockWidgetFactoryBase
from .krita_shape_ui import KritaShapeUIDocker


Krita.instance().addDockWidgetFactory(
    DockWidgetFactory("shape_ui_docker",
                      DockWidgetFactoryBase.DockRight,
                      KritaShapeUIDocker))

