
import sys
import logging

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit

from p4p import Value
from p4p.client.PyQt import Context, Disconnected

_log = logging.getLogger(__name__)

class Demo(QWidget):
    def __init__(self, pvname):
        QWidget.__init__(self)
        self._pvname = pvname
        self.initUI()

        self._put = None # in-progress put

        self.pvname.setText(pvname)

        self.ctxt = Context('pva', parent=self)
        self.ctxt.monitor(pvname, self._update, limitHz=1.0)

        self.edit.returnPressed.connect(self.doPut)

    def initUI(self):
        layout = QVBoxLayout()

        self.pvname = QLabel(self)
        self.pvname.setText("<name>")
        layout.addWidget(self.pvname)

        self.value = QLabel(self)
        self.value.setText("<Connecting>")
        layout.addWidget(self.value)

        self.edit = QLineEdit(self)
        layout.addWidget(self.edit)

        self.error = QLabel(self)
        self.error.setText("<Connecting>")
        layout.addWidget(self.error)

        self.setLayout(layout)
        self.setGeometry(200, 200, 250, 150)

    def _update(self, V):
        _log.debug('_update %s %s', type(V), V)
        if isinstance(V, Disconnected):
            self.value.setText("<???>")
        elif isinstance(V, Exception):
            self.value.setText("<!!!>")
            self.error.setText(str(V))
        else:
            self.value.setText(str(V))

    def doPut(self):
        _log.debug('Put triggered')
        try:
            self.ctxt.put(self._pvname, self.edit.text(), self.donePut)
        except:
            _log.exception('put')

    def donePut(self, V):
        if V is None:
            self.error.setText("Put complete")
        else:
            self.error.setText(str(V))

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    demo = Demo(app.arguments()[1])
    demo.show()
    sys.exit(app.exec_())
