import requests
from bs4 import BeautifulSoup
from globals import base_path


class OpenOrders:
    def __init__(self, open_orders_path, headers):
        self.open_orders_path = open_orders_path
        self.headers = headers

    def _get_orders(self, order_type: str):
        order_list = []
        url = f"{self.open_orders_path}/{order_type}"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            rows = soup.find("tbody").find_all("tr")
            for row in rows:
                player_name = row.contents[3].text.strip()
                posted_price = row.contents[5].text.strip().replace(",", "")
                order_id = row.get("id")
                player_url = "https://mlb23.theshow.com" + row.find("a")["href"].strip()

                order_list.append(
                    {
                        "Name": player_name,
                        "Posted Price": posted_price,
                        "URL": player_url,
                        "Order ID": order_id,
                    }
                )
        except AttributeError:
            pass

        return order_list

    def get_buy_orders(self):
        return self._get_orders("buy_orders")

    def get_sell_orders(self):
        return self._get_orders("sell_orders")

    def get_all_open_orders(self):
        return self.get_buy_orders() + self.get_sell_orders()
