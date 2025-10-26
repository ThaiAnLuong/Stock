import sys
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5 import uic
from PyQt5.uic import loadUi

import pandas as pd

class Visualization(QMainWindow):
    def __init__(self):
        super(Visualization, self).__init__()
        loadUi('visualization.ui', self)
        self.setWindowTitle("Visualization")

        # Connect the findButton click event to the update_graph function
        self.searchButton.clicked.connect(self.update_graph)

        # Initialize with a default stock symbol
        self.current_symbol = ""
        self.update_graph()

    def update_graph(self):
        # Get the stock symbol from the findStock lineEdit
        new_symbol = self.findStock.text().upper()

        # Use the new symbol if provided; otherwise, use the default symbol
        symbol = new_symbol if new_symbol else self.current_symbol

        # Update the current symbol
        self.current_symbol = symbol

        # Replace with the URL of your Flask service, including the symbol parameter
        url = f"http://127.0.0.1:5000/?symbol={symbol}"

        # Fetch JSON data from the Flask service
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)

            # Access the new JSON structure
            stock_data = data["stock_data"]

            # Parse JSON data into a DataFrame
            df = pd.DataFrame(stock_data)

            # Convert the "Date" column to datetime format
            df["Date"] = pd.to_datetime(df["Date"])

            # Clear the existing layout before adding the new graph
            layout = self.stockData.layout()
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

            # Create a Figure and Axes for the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df["Date"], df["Close"], marker="o", linestyle="-")
            ax.set_title(f"Stock Price for {data['symbol']}")  # Use the actual stock symbol or name
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.grid(True)

            # Create a FigureCanvas
            canvas = FigureCanvas(fig)

            # Add the FigureCanvas to the layout
            layout.addWidget(canvas)
        else:
            print(f"Error: Unable to fetch data for symbol {symbol} from the Flask service.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
