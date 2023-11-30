from PySide6.QtWidgets import QApplication
import os
import sys
from menu import Menu

# Clears Console using command
os.system('cls' if os.name == 'nt' else 'clear')

# Create an instance of the application
class main(QApplication):
    def __init__(self):
        super().__init__()
        self.window = Menu()
        self.window.show()
        self.exec()
        
# Run the application
if __name__ == "__main__":
    app = main()
    sys.exit(app.exit())