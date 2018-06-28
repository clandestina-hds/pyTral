import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from modules.mainView import mainView

class principal(QMainWindow):
    
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle('pyTral')
        self.table_widget = mainView(self)
        self.setCentralWidget(self.table_widget)
        self.showMaximized()
        self.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = principal()
    sys.exit(app.exec_())