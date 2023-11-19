import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, QDialog

class GPTDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set the dimensions of the dialog
        self.setGeometry(200, 200, 300, 100)

        # Create widgets for the dialog
        self.gpt_edit = QLineEdit(self)
        gpt_button = QPushButton("send", self)

        # Create layout for the dialog
        layout = QVBoxLayout(self)
        layout.addWidget(self.gpt_edit)
        layout.addWidget(gpt_button)

        # Connect the search button to a function
        gpt_button.clicked.connect(self.chat_clicked)

    def chat_clicked(self):
        chat_text = self.gpt_edit.text()
        print(f"message: {chat_text}")

        self.accept()
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set the dimensions of the dialog
        self.setGeometry(200, 200, 300, 100)

        # Create widgets for the dialog
        self.search_edit = QLineEdit(self)
        search_button = QPushButton("Search", self)

        # Create layout for the dialog
        layout = QVBoxLayout(self)
        layout.addWidget(self.search_edit)
        layout.addWidget(search_button)

        # Connect the search button to a function
        search_button.clicked.connect(self.search_clicked)

    def search_clicked(self):
        search_text = self.search_edit.text()
        print(f"Searching for: {search_text}")

        self.accept()
class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 500)

        # Create buttons
        button1 = QPushButton("PDF", self)
        button2 = QPushButton("Email", self)
        button3 = QPushButton("Wikipedia", self)
        button4 = QPushButton("ChatGPT", self)

        button1.setFixedSize(200, 100)
        button2.setFixedSize(200, 100)
        button3.setFixedSize(200, 100)
        button4.setFixedSize(200, 100)

        font = button1.font()
        font.setPointSize(16)
        button1.setFont(font)
        button2.setFont(font)
        button3.setFont(font)
        button4.setFont(font)

        # Create a layout and set it for the main window
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(50)
        self.setLayout(grid_layout)

        # Add buttons to the layout in a 2 by 2 grid
        grid_layout.addWidget(button1, 0, 0)
        grid_layout.addWidget(button2, 0, 1)
        grid_layout.addWidget(button3, 1, 0)
        grid_layout.addWidget(button4, 1, 1)

        # Set up connections if needed
        button1.clicked.connect(self.button1_clicked)
        button2.clicked.connect(self.button2_clicked)
        button3.clicked.connect(self.button3_clicked)
        button4.clicked.connect(self.button4_clicked)

        # Define functions to be called when buttons are clicked
    def button1_clicked(self):
        print("Button 1 clicked!")

    def button2_clicked(self):
        print("Button 2 clicked!")

    def button3_clicked(self):
        search_dialog = SearchDialog()
        search_dialog.exec_()

    def button4_clicked(self):
        gpt_dialog = GPTDialog()
        gpt_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec_())
