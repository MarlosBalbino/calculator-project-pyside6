import math
import sys
from qt_core import *

from solver import LinearSolver

class MyLineEdit(QLineEdit):
    def __init__(self, background_color="#44475a"):
        super().__init__()
        self.setStyleSheet(f"""
                        background-color: {background_color}; 
                        font-family: Fira Code;
                        font: bold;
                        color: white;
                        font-size: 12pt;
                        border-radius: 4px;
                        border: none;
                        """
                    )
        self.setMaximumSize(200, 200)

class MatrixFrame(QFrame):
    def __init__(self, dim: int = 3):
        super().__init__()
        self.dim = dim
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(30)

        self.frame1 = QFrame()
        self.grid_layout = QGridLayout(self.frame1)
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.grid_layout.setSpacing(20)

        self.frame2 = QFrame()
        self.vertical_layout = QVBoxLayout(self.frame2)
        self.vertical_layout.setContentsMargins(0,0,0,0)
        self.vertical_layout.setSpacing(20)

        self.load(dim)
        

    def load(self, dim):
        self.dim = dim
        for widget in self.frame1.findChildren(QLineEdit):
            widget.deleteLater()

        for widget in self.frame2.findChildren(QLineEdit):
            widget.deleteLater()

        for i in range(dim):
            for j in range(dim):
                line_edit = MyLineEdit()                
                self.grid_layout.addWidget(line_edit, i, j)

        for i in range(dim):
            line_edit = MyLineEdit(background_color="#6272a4")
            self.vertical_layout.addWidget(line_edit)

        self.main_layout.addWidget(self.frame1)
        self.main_layout.addWidget(self.frame2)


    def get_values(self) -> tuple:
        matrix_values = [float(widget.text()) for widget in self.frame1.findChildren(QLineEdit)]
        matrix = []
        k = 0
        for i in range(self.dim):
            line = []
            for j in range(self.dim):
                value = matrix_values[k]
                print(value)
                line.append(value)
                k += 1
            matrix.append(line)

        idependents_coeficients = [float(widget.text()) for widget in self.frame2.findChildren(QLineEdit)]
        return matrix, idependents_coeficients


class Display(QFrame):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(200)
        self.layout = QVBoxLayout(self)
        self.label = QLabel()
        self.label.setFixedHeight(30)
        self.label.setText("Soluções:")
        self.label.setStyleSheet("""
                    font-family: Fira Code;
                    font: bold;
                    color: white;
                    font-size: 12pt;                    
                    """
        )

        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("""
                    font-family: Fira Code;
                    font: bold;
                    color: white;
                    font-size: 16pt;
                    border: none;                  
                    """
        )
        self.text_edit.setReadOnly(True)
        self.text_edit.setText("0")
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_edit)

class MyButton(QPushButton):
    def __init__(
            self, 
            text=None,
            background_color="#44475a",
            hover_color="#6272a4",
            pressed_color="#c3ccdf"):
        super().__init__(text=text)

        style = f"""
        QPushButton{{
            background-color: {background_color}; color: white;
            font: bold;
            font-family: Fira Code;
            font-size: 12pt;
            border-radius: 4px;
            border: none;
        }}
        QPushButton::hover{{            
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {pressed_color};
        }}
        """
        self.setStyleSheet(style)
        self.setMaximumHeight(200)
        self.setMinimumWidth(60)


class ButtonsFrame(QFrame):

    def __init__(self):
        super().__init__()
        self.layout_ = QGridLayout(self)
        self.layout_.setSpacing(5)

        txts = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "/", "<|", "|>", "Enter"]
        self.btns = []

        k = 0
        for i in range(math.ceil(len(txts)/3)):
            for j in range(3):
                try:
                    txt = txts[k]
                    if txt == "":
                        self.layout_.addWidget(QFrame(), i, j)
                    else:
                        btn = MyButton(txt)                        
                        self.layout_.addWidget(btn, i, j)
                        self.btns.append(btn)
                except IndexError:
                    break
                k+=1

  
class Separator(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white")
        self.setFixedHeight(1)


class DimSelector(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(50)
        self.layout_ = QHBoxLayout(self)
      
        self.btn2x2 = MyButton("2X2")
        self.btn3x3 = MyButton("3X3")
        self.btn4x4 = MyButton("4X4")
        self.btnNxN = MyLineEdit(background_color="#6272a4")
        self.btnNxN.setText("NxN")
        self.btnOk = MyButton("Ok")

        self.layout_.addWidget(self.btn2x2)
        self.layout_.addWidget(self.btn3x3)
        self.layout_.addWidget(self.btn4x4)
        self.layout_.addWidget(self.btnNxN)
        self.layout_.addWidget(self.btnOk)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()        
        self.resize(380, 760)
        
        self.main_widget = QWidget()
        self.main_widget.setStyleSheet("background-color: #343644")
        self.main_layout = QVBoxLayout(self.main_widget)

        separator0 = Separator()
        separator1 = Separator()
        separator2 = Separator()
        self.dim_selector = DimSelector()
        self.matrix_frame = MatrixFrame()
        self.display_frame = Display()
        self.buttons_frame = ButtonsFrame()

        self.main_layout.addWidget(self.display_frame)
        self.main_layout.addWidget(separator2)
        self.main_layout.addWidget(self.dim_selector)
        self.main_layout.addWidget(separator0)
        self.main_layout.addWidget(self.matrix_frame)
        self.main_layout.addWidget(separator1)        
        self.main_layout.addWidget(self.buttons_frame)

        self.setCentralWidget(self.main_widget)
        self.handle()

    def handle(self):
        self.D: list
        self.I: list

        self.dim_selector.btn2x2.clicked.connect(lambda: self.matrix_frame.load(2))
        self.dim_selector.btn3x3.clicked.connect(lambda: self.matrix_frame.load(3))
        self.dim_selector.btn4x4.clicked.connect(lambda: self.matrix_frame.load(4))
        self.dim_selector.btnOk.clicked.connect(lambda: self.load_handle())
    
        enter_btn: QPushButton = self.buttons_frame.btns[14]
        enter_btn.clicked.connect(self.solve)

    def load_handle(self):
        dim = int(self.dim_selector.btnNxN.text())
        self.matrix_frame.load(dim)
        
    def solve(self):
        D, I = self.matrix_frame.get_values()
    
        solve = LinearSolver()
        solve.cramer(D, I)
        solutions = solve.get_solutions()

        self.display_frame.text_edit.clear()
        if not solutions:
            self.display_frame.text_edit.insertPlainText("Erro: Sistema impossível ou indeterminado!!")
        for solution in solutions:
            self.display_frame.text_edit.insertPlainText(str(solution))
            self.display_frame.text_edit.insertPlainText("\n")
















if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())