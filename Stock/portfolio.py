from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QWidget, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from cloudant.client import Cloudant
import requests

class Portfolio(QMainWindow):
    def __init__(self):
        super(Portfolio, self).__init__()
        loadUi('portfolio.ui', self)
        self.setWindowTitle("Portfolio")


        # data.create_document({"_id": "test", "username": "test", "stocks": [{"stock": "APPL", "shares": 6}, {"stock": "GAE", "shares": 12}]})

        self.searchButton.clicked.connect(self.stock_search)
        self.buyButton.clicked.connect(self.on_buy_clicked)
        self.sellButton.clicked.connect(self.on_sell_clicked)

        self.stock_data = {

        }

        self.load_user_stock_data()
        self.populate_stock_list()

        total_price = self.calculate_portfolio_total()
        self.totalPrice.setText(f"{total_price:.2f}" if total_price is not None else "0.00")

    def load_user_stock_data(self):
       from loginManagement import LoginApp

       self.API_USER = "3fdf89c0-70ae-421c-8a5c-f3f07abc3988-bluemix"
       self.API_KEY = "IGzHN-SnHoE7X-Xn_wlCK0ogL62UusTafB2ZO8CZeXub"

       client = Cloudant.iam(self.API_USER, self.API_KEY, connect=True)
       data = client["portfolio"]

       # Get the username from your application
       username = LoginApp.username

       # Check if the user exists in the database
       if LoginApp.username in data:
           existing_user = True
           user_doc = data[LoginApp.username]
       else:
           existing_user = False

       if existing_user:
           # User exists, retrieve the stock data
           user_stocks = user_doc.get("stocks", [])
           for stock in user_stocks:
               stock_symbol = stock.get("stock")
               shares = stock.get("shares")
               # Fetch stock price and other information (you may need to modify this based on your implementation)
               # For now, we'll set a placeholder price for each stock
               stock_price = 100.0  # Placeholder value
               self.stock_data[stock_symbol] = {'price': stock_price, 'shares': shares}

    def populate_stock_list(self):
        self.stockList.clear()
        unique_stocks = {}
        for symbol, data in self.stock_data.items():
            if symbol in unique_stocks:
                unique_stocks[symbol]['shares'] += data['shares']
            else:
                unique_stocks[symbol] = {'price': data['price'], 'shares': data['shares']}

        for symbol, data in unique_stocks.items():
            price = data['price']
            shares = data['shares']
            item = QListWidgetItem(f"{symbol}: ${price:.2f} | Shares: {shares}")
            self.stockList.addItem(item)

    def on_search_clicked(self):
        # Implement code to search for stocks
        stock_symbol = self.search_line_edit.text()
        # Use stock_symbol to fetch stock information (e.g., from an API)
        # Update the information in the model or update the list widget

    def on_buy_clicked(self):
        from loginManagement import LoginApp

        self.API_USER = "3fdf89c0-70ae-421c-8a5c-f3f07abc3988-bluemix"
        self.API_KEY = "IGzHN-SnHoE7X-Xn_wlCK0ogL62UusTafB2ZO8CZeXub"

        client = Cloudant.iam(self.API_USER, self.API_KEY, connect=True)
        data = client["portfolio"]

        # Implement code to buy stocks
        stock_symbol = self.stockToFind.text().upper()  # Use the correct field from your UI
        num_shares_str = self.numShares.text()

        # Check if the user entered a valid number of shares
        if not num_shares_str.isdigit() or int(num_shares_str) <= 0:
            QMessageBox.information(self, "Alert", "Please enter a valid number of shares.", QMessageBox.Ok)
            return

        num_shares = int(num_shares_str)

        # Get the price from the label
        price_str = self.price.text()
        company_name = self.company.text()

        if price_str == "None" or company_name == "None":
            QMessageBox.information(self, "Alert", "Stock information is not available. Please search for a valid stock.", QMessageBox.Ok)
            return

        price = float(price_str)

        print(f"Buying {num_shares} shares of {stock_symbol} at ${price:.2f} each")

        # Update the model or add the purchased stock to the data
        if stock_symbol in self.stock_data:
            self.stock_data[stock_symbol]['shares'] += num_shares
        else:
            # Handle the case when the stock is not in the initial data
            self.stock_data[stock_symbol] = {'price': price, 'shares': num_shares}

        # Update the database
        username = "test"  # You may need to get the username from your application
        user_data = {"_id": LoginApp.username, "username": LoginApp.username, "stocks": []}

        # Check if the user already exists in the database
        if LoginApp.username in data:
            existing_user = True
            user_doc = data[LoginApp.username]
            print(data[LoginApp.username])
        else:
            existing_user = False

        if existing_user:
            # User exists, update the stocks list
            existing_user_stocks = user_doc.get("stocks", [])
            stock_exists = False
            for user_stock in existing_user_stocks:
                if user_stock["stock"] == stock_symbol:
                    user_stock["shares"] += num_shares
                    stock_exists = True
                    break

            if not stock_exists:
                existing_user_stocks.append({"stock": stock_symbol, "shares": num_shares})

            user_data["stocks"] = existing_user_stocks
            user_doc.save()
        else:
            # User doesn't exist, create a new document
            user_data["stocks"] = [{"stock": stock_symbol, "shares": num_shares}]
            data.create_document(user_data)

        # Update the displayed list in the UI
        self.populate_stock_list()

        # Clear the search line edit and numShares line edit
        self.stockToFind.clear()
        self.numShares.clear()

        # Clear the labels
        self.price.clear()
        self.company.clear()

        # Optionally, update the total price as well
        total_price = self.calculate_portfolio_total()
        self.totalPrice.setText(f"{total_price:.2f}" if total_price is not None else "0.00")


    def on_sell_clicked(self):
        from loginManagement import LoginApp

        self.API_USER = "3fdf89c0-70ae-421c-8a5c-f3f07abc3988-bluemix"
        self.API_KEY = "IGzHN-SnHoE7X-Xn_wlCK0ogL62UusTafB2ZO8CZeXub"

        client = Cloudant.iam(self.API_USER, self.API_KEY, connect=True)
        data = client["portfolio"]

        # Get the selected item from the list view
        selected_item = self.stockList.currentItem()
        if not selected_item:
            QMessageBox.information(self, "Alert", "Please select a stock to sell.", QMessageBox.Ok)
            return

        # Extract stock information from the selected item
        selected_text = selected_item.text()
        parts = selected_text.split(':')
        stock_symbol = parts[0].strip()

        # Check if the user entered a valid number of shares
        num_shares_str = self.sharesToSell.text()
        if not num_shares_str.isdigit() or int(num_shares_str) <= 0:
            QMessageBox.information(self, "Alert", "Please enter a valid number of shares.", QMessageBox.Ok)
            return

        num_shares = int(num_shares_str)

        # Check if the stock exists in the user's portfolio
        if stock_symbol not in self.stock_data:
            QMessageBox.information(self, "Alert", "Stock not found in your portfolio.", QMessageBox.Ok)
            return

        # Check if the user has enough shares to sell
        if self.stock_data[stock_symbol]['shares'] < num_shares:
            QMessageBox.information(self, "Alert", "Insufficient shares to sell.", QMessageBox.Ok)
            return

        # Update the model or subtract the sold stock from the data
        self.stock_data[stock_symbol]['shares'] -= num_shares

        # Update the database
        username = LoginApp.username
        user_data = {"_id": username, "username": username, "stocks": []}

        # Check if the user already exists in the database
        if LoginApp.username in data:
            existing_user = True
            user_doc = data[LoginApp.username]
        else:
            existing_user = False

        if existing_user:
            # User exists, update the stocks list
            existing_user_stocks = user_doc.get("stocks", [])
            for user_stock in existing_user_stocks:
                if user_stock["stock"] == stock_symbol:
                    user_stock["shares"] -= num_shares
                    # Remove the stock entry if shares become zero
                    if user_stock["shares"] <= 0:
                        existing_user_stocks.remove(user_stock)
                    break
        user_doc.save()

        # Update the displayed list in the UI
        self.populate_stock_list()

        # Clear the search line edit and numShares line edit
        self.stockToFind.clear()
        self.numShares.clear()

        # Clear the labels
        self.price.clear()
        self.company.clear()

        # Optionally, update the total price as well
        total_price = self.calculate_portfolio_total()
        self.totalPrice.setText(f"{total_price:.2f}" if total_price is not None else "0.00")


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
            company_name = stock_info.get('Company Name', '')
            current_price = stock_info.get('Current Price', 0.0)

            if(f"{company_name}" == "None"):
                QMessageBox.information(self, "Alert", "Stock Does Not Exist", QMessageBox.Ok)
                return

            self.price.setText(f"{current_price}")
            self.company.setText(f"{company_name}")

        else:
            print(f"Error: {response.status_code}")
            QMessageBox.information(self, "Alert", "Stock Does Not Exist", QMessageBox.Ok)
            return

    def calculate_portfolio_total(self):
           total_value = 0
           for symbol, data in self.stock_data.items():
               price = data['price']
               shares = data['shares']
               total_value += price * shares
           return total_value

if __name__ == "__main__":
    app = QApplication([])
    window = Portfolio()
    window.show()
    print("User's Portfolio Total:", window.calculate_portfolio_total())
    app.exec_()
