from qtpy.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
    )

import sys
import sympy as sp

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtPy Calc")
        self.resize(300, 400)
        self.angle_mode = "DEG"
        self._t = sp.symbols("_t")
        self.local_dict = self._build_locals()
        self.init_ui()
        

    def _build_locals(self):
        #rebuild sympify locals based on angle mode
        if self.angle_mode == "DEG":
            sin = sp.Lambda(self._t, sp.sin(sp.pi*self._t/180))
            cos = sp.Lambda(self._t, sp.cos(sp.pi*self._t/180))
            tan = sp.Lambda(self._t, sp.tan(sp.pi*self._t/180))
            asin = sp.Lambda(self._t, 180/sp.pi * sp.asin(self._t))
            acos = sp.Lambda(self._t, 180/sp.pi * sp.acos(self._t))
            atan = sp.Lambda(self._t, 180/sp.pi * sp.atan(self._t))
        else: #if self.angle_mode = "RAD"
            sin, cos, tan = sp.sin, sp.cos, sp.tan
            asin, acos, atan = sp.asin, sp.acos, sp.atan

        return {
            #trig functions
            "sin": sin, "cos": cos, "tan": tan,
            "asin": asin, "acos": acos, "atan": atan,
            #roots, exponents, logs
            "sqrt": sp.sqrt, "exp": sp.exp, "log": sp.log, "ln": sp.log,
            #constants
            "pi": sp.pi, "E": sp.E, "e": sp.E,
            }
        

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

        #top row utility buttons
        self.mode_btn = QPushButton(self.angle_mode) #Toggle deg/rad
        self.mode_btn.clicked.connect(self.toggle_angle_mode)
        self.mode_btn.setMinimumSize(60, 60)
        grid.addWidget(self.mode_btn, 0, 0)

        pi_btn = QPushButton("π")
        pi_btn.clicked.connect(lambda _=False: self.on_button_click("π"))
        pi_btn.setMinimumSize(60, 60)
        grid.addWidget(pi_btn, 0, 1)

        e_btn = QPushButton("e")
        e_btn.clicked.connect(lambda _=False: self.on_button_click("e"))
        e_btn.setMinimumSize(60, 60)
        grid.addWidget(e_btn, 0, 2)

        #button grid with wide 0 and = button
        buttons = [
            #scientific rows
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('log', 1, 3), 
            ('sqrt', 2, 0), ('exp', 2, 1), ('(', 2, 2), (')', 2, 3),
            #std calc rows
            ('7', 3, 0),('8', 3, 1),('9', 3, 2), ('/', 3, 3),
            ('4', 4, 0),('5', 4, 1), ('6', 4, 2),('*', 4, 3),
            ('1', 5, 0), ('2', 5, 1),('3', 5, 2),('-', 5, 3),
            ('0', 6, 0),('.', 6, 1), ('=', 6, 2),('+', 6, 3),
            ('C', 8, 0, 1, 2),
            ]

        # create buttons and add them to the grid
        for label, row, col, *rest in buttons:
            rowspan = rest[0] if len(rest) > 0 else 1
            colspan = rest[1] if len(rest) > 1 else 1
            button = QPushButton(label)
            button.setMinimumSize(60, 60)
            grid.addWidget(button, row, col, rowspan, colspan)
            button.clicked.connect(lambda checked, text=label: self.on_button_click(text))

        # make rows and columns stretch propotionally
        for i in range(4):
            grid.setColumnStretch(i, 1)

        for j in range(8):
            grid.setRowStretch(j, 1)

        # add space above and below the grid for vertical centering
        vbox.addStretch(1)
        vbox.addLayout(grid)
        vbox.addStretch(1)

    def toggle_angle_mode(self):
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self.mode_btn.setText(self.angle_mode)
        self.local_dict = self._build_locals()

    def on_button_click(self, text):
        if text == 'C':
            self.display.clear()
        elif text == '=':
            expression = self.display.text()
            self.calculate(expression)
        elif text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sqrt', 'log', 'exp']:
            self.display.setText(self.display.text() + text + '(')
        elif text == 'π':
            self.display.setText(self.display.text() + 'pi')
        elif text == 'e':
            self.display.setText(self.display.text() + 'E')
        else:
            self.display.setText(self.display.text() + text)

    def calculate(self, expression):
        try:
            # parse expression with sympy
            expr = sp.sympify(expression, locals=self.local_dict)
            result = sp.N(expr) #numerical evaluation
            self.display.setText(str(result))
        except Exception:
            self.display.setText("Error")

    def keyPressEvent(self, event):
        key = event.text()
        if key.isdigit() or key in ['+', '-', '*', '/', '.']:
            self.on_button_click(key)
        elif event.key() == 16777220: # enter key
            self.on_button_click('=')
        elif event.key() == 16777221: # enter on numpad
            self.on_button_click('=')
        elif event.key() == 16777219:
            self.display.setText(self.display.text()[:-1])
        elif key.upper() == 'C': # clear with c
            self.on_button_click('C')
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
