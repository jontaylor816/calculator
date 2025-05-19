from qtpy.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
    )

import sys

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtPy Calc")
        self.resize(300, 400)
        self.init_ui()

    def init_ui(self):
        #main layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        #display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px;")
        self.display.setFixedHeight(50)
        vbox.addWidget(self.display)

        #button grid
        grid = QGridLayout()
        vbox.addLayout(grid)

        #button grid with wide 0 and = button
        buttons = [
            ('7', 1, 0),
            ('8', 1, 1),
            ('9', 1, 2),
            ('/', 1, 3),
            ('4', 2, 0),
            ('5', 2, 1),
            ('6', 2, 2),
            ('*', 2, 3),
            ('1', 3, 0),
            ('2', 3, 1),
            ('3', 3, 2),
            ('-', 3, 3),
            ('0', 4, 0, 1 , 2),
            ('.', 4, 2),
            ('+', 4, 3),
            ('C', 5, 0),
            ('=', 5, 1, 1, 3)
            ]

        # create buttons and add them to the grid
        for label, row, col, *rest in buttons:
            rowspan = rest[0] if len(rest) > 0 else 1
            colspan = rest[1] if len(rest) > 1 else 1
            button = QPushButton(label)
            button.setMinimumSize(60, 60)
            grid.addWidget(button, row, col, rowspan, colspan)

        # make rows and columns stretch propotionally
        for i in range(4):
            grid.setColumnStretch(i, 1)

        for j in range(5):
            grid.setRowStretch(j, 1)

        # add space above and below the grid for vertical centering
        vbox.addStretch(1)
        vbox.addLayout(grid)
        vbox.addStretch(1)

        def on_button_click(self, text):
            if text == 'C':
                self.display.clear()
            elif text == '=':
                expression = self.display.text()
                self.calculate(expression)
            else:
                self.display.setText(self.display.text() + text)

        def calculate(self, expression):
            try:
                import numpy as np
                # evaluate expression using numpy's namespace
                result = str(eval(expression, {"__builtins__": None}, vars(np)))
                self.display.setText(result)
            except Exception:
                self.display.setText("Error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
