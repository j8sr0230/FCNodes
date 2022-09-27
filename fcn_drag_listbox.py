from qtpy.QtGui import QPixmap, QIcon, QDrag
from qtpy.QtCore import QSize, Qt, QByteArray, QDataStream, QMimeData, QIODevice, QPoint
from qtpy.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem

from nodeeditor.utils import dumpException

from fcn_conf import NodesStore, LISTBOX_MIMETYPE


class QDMDragListbox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.add_my_items()

    def refresh_ui(self):
        self.clear()
        self.add_my_items()

    def add_my_items(self):
        for key in NodesStore.nodes:
            node = NodesStore.get_class_from_opcode(key)
            self.add_my_item(node.op_title, node.icon, node.op_code)

    def add_my_item(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self)  # Can be (icon, text, parent, <int>type)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)

    def startDrag(self, *args, **kwargs):
        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)
            pixmap = QPixmap(item.data(Qt.UserRole))

            item_data = QByteArray()
            data_stream = QDataStream(item_data, QIODevice.WriteOnly)
            data_stream << pixmap
            data_stream.writeQString(op_code)
            data_stream.writeQString(item.text())
            mime_data = QMimeData()
            mime_data.setData(LISTBOX_MIMETYPE, item_data)

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
            drag.setPixmap(pixmap)
            drag.exec_(Qt.MoveAction)

        except Exception as e:
            dumpException(e)
