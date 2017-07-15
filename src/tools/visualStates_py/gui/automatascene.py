
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from enum import Enum
from . import guistate, guitransition

class AutomataScene(QGraphicsScene):

    # slots
    stateInserted = pyqtSignal('QGraphicsItem')
    transitionInserted = pyqtSignal('QGraphicsItem')

    def __init__(self, parent=None):
        super().__init__(parent)

        self.operationType = None

        # transition origin and destination
        self.origin = None
        self.destination = None

        self.stateIndex = -1
        self.transitionIndex = -1


    def mousePressEvent(self, qGraphicsSceneMouseEvent):
        super().mousePressEvent(qGraphicsSceneMouseEvent)



    def mouseReleaseEvent(self, qGraphicsSceneMouseEvent):
        if self.operationType == OpType.ADDSTATE and qGraphicsSceneMouseEvent.button() == Qt.LeftButton:
            selectedItems = self.items(qGraphicsSceneMouseEvent.scenePos())
            if len(selectedItems) == 0:
                sIndex = self.getStateIndex()
                stateItem = guistate.StateGraphicsItem(sIndex, 0, None, qGraphicsSceneMouseEvent.scenePos().x(), qGraphicsSceneMouseEvent.scenePos().y(), False, 'state ' + str(sIndex))
                self.addItem(stateItem)
                self.stateInserted.emit(stateItem)
            self.origin = None
        elif self.operationType == OpType.ADDTRANSITION and qGraphicsSceneMouseEvent.button() == Qt.LeftButton:
            selectedItems = self.items(qGraphicsSceneMouseEvent.scenePos())
            print('selectedItems.len=' + str(len(selectedItems)))
            if len(selectedItems) > 0:
                # get the parent
                item = self.getParentItem(selectedItems[0])
                if isinstance(item, guistate.StateGraphicsItem):
                    if self.origin != None:
                        self.destination = item
                        tIndex = self.getTransitionIndex()
                        tranItem = guitransition.TransitionGraphicsItem(self.origin, self.destination, tIndex, 'transition ' + str(tIndex))
                        self.addItem(tranItem)
                        self.origin = None
                        self.destination = None
                        self.transitionInserted.emit(tranItem)
                        print('a new transition is added.')
                    else:
                        self.origin = item
                else:
                    self.origin = None
            else:
                self.origin = None

        super().mouseReleaseEvent(qGraphicsSceneMouseEvent)

    def setOperationType(self, type):
        self.operationType = type


    def getStateIndex(self):
        self.stateIndex += 1
        return self.stateIndex


    def getTransitionIndex(self):
        self.transitionIndex += 1
        return self.transitionIndex


    def dragEnterEvent(self, QGraphicsSceneDragDropEvent):
        print('scene drag enter event')



    def dragMoveEvent(self, QGraphicsSceneDragDropEvent):
        print('scene drag move event')


    def getParentItem(self, item):
        while item.parentItem() != None:
            item = item.parentItem()
        return item


class OpType(Enum):
    ADDSTATE = 0
    ADDTRANSITION = 1

