import sys
from PyQt5.QtWidgets import QApplication
from loginManagement import LoginApp  # Import your MainWindow class from its module
from visualization import Visualization
from portfolio import Portfolio

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of your MainWindow class
    main_window = LoginApp()

    # Show the main window
    main_window.show()

    # Run the application event loop
    sys.exit(app.exec_())
