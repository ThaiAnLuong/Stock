from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5.uic import loadUi
import requests

class findStock(QMainWindow):
    def __init__(self):
        super(findStock, self).__init__()
        loadUi('StockPrice.ui', self)

        # Connect the clicked signal of findButton to the stock_search method
        self.findButton.clicked.connect(self.stock_search)

    def stock_search(self):
        symbol = self.stockToFind.text()
        # URL of the Flask application
        url = f"https://findstock.1ao2e0vnln8d.ca-tor.codeengine.appdomain.cloud/search_stock/{symbol}"

#        Sending a GET request to the Flask application
        response = requests.get(url)

#        Checking if the request was successful
        if response.status_code == 200:
            # Extracting information from the JSON response
            data = response.json()
            stock_info = data.get('stock_info', {})

            # Assigning values to variables with the same names
            week_range = stock_info.get('52 Week Range', '')
            average_volume = stock_info.get('Average Volume', 0)
            company_name = stock_info.get('Company Name', '')
            current_price = stock_info.get('Current Price', 0.0)
            day_range = stock_info.get("Day's Range", '')
            dividend_yield = stock_info.get('Dividend Yield', None)
            market_cap = stock_info.get('Market Cap', 0)
            open_price = stock_info.get('Open Price', 0.0)
            pe_ratio = stock_info.get('P/E Ratio', 0.0)
            previous_close = stock_info.get('Previous Close', 0.0)
            volume = stock_info.get('Volume', 0)

            if(f"{company_name}" == "None"):
                QMessageBox.information(self, "Alert", "Stock Does Not Exist", QMessageBox.Ok)
                return

            self.showPrice.setText(f"{current_price}")
            self.companyName.setText(f"{company_name}")
            self.showOpen.setText(f"{open_price}")
            self.showPreClose.setText(f"{previous_close}")
            self.showDayRange.setText(f"{day_range}")
            self.showAvgVol.setText(f"{average_volume}")
            self.showWeekRange.setText(f"{week_range}")
            self.showVolume.setText(f"{volume}")
        else:
            print(f"Error: {response.status_code}")
            QMessageBox.information(self, "Alert", "Stock Does Not Exist", QMessageBox.Ok)
            return

