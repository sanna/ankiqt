# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import ankiqt
from anki.utils import parseTags, joinTags

class ActiveTagsChooser(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.dialog = ankiqt.forms.activetags.Ui_Dialog()
        self.dialog.setupUi(self)
        self.connect(self.dialog.buttonBox, SIGNAL("helpRequested()"),
                     self.onHelp)
        self.rebuildTagList()


    def rebuildTagList(self):
        self.tags = self.parent.deck.allTags()
        self.tags.sort()
        self.items = []
        self.suspended = {}
        for t in parseTags(self.parent.deck.suspended):
            self.suspended[t] = 1
        for t in self.tags:
            item = QListWidgetItem(t, self.dialog.list)
            self.dialog.list.addItem(item)
            self.items.append(item)
            idx = self.dialog.list.indexFromItem(item)
            if t in self.suspended:
                mode = QItemSelectionModel.Deselect
            else:
                mode = QItemSelectionModel.Select
            self.dialog.list.selectionModel().select(idx, mode)

    def accept(self):
        n = 0
        suspended = []
        for item in self.items:
            idx = self.dialog.list.indexFromItem(item)
            if not self.dialog.list.selectionModel().isSelected(idx):
                suspended.append(self.tags[n])
            n += 1
        self.parent.deck.suspended = joinTags(suspended + ["Suspended"])
        self.parent.deck.setModified()
        self.parent.reset()
        QDialog.accept(self)

    def onHelp(self):
        QDesktopServices.openUrl(QUrl(ankiqt.appWiki +
                                      "ActiveTags"))


def show(parent):
    at = ActiveTagsChooser(parent)
    at.exec_()