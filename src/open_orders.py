import requests
from bs4 import BeautifulSoup
from globals import base_path

# CHANGE THIS TO CLASS -> CAN USE CLASS WITH ATTRIBUTES INSTEAD OF DICTIONARY


def get_open_buy_orders_list(data):
    buy_orders = []
    open_orders_page = requests.get(base_path + "orders/buy_orders", headers=data)
    soup = BeautifulSoup(open_orders_page.text, "html.parser")

    try:
        orders_list = soup.find("tbody")
        open_order = orders_list.find_all("tr")
        for each in open_order:
            player_dict = {}
            player_name = each.contents[3].text.strip()
            posted_price = each.contents[5].text.strip().replace(",", "")
            order_id = each.get("id")
            player_url = each.find("a")
            player_url = (
                "https://mlb23.theshow.com" + player_url["href"].lstrip().rstrip()
            )
            player_dict["Name"] = player_name
            player_dict["Posted Price"] = posted_price
            player_dict["URL"] = player_url
            player_dict["Order ID"] = order_id
            buy_orders.append(player_dict)

        return buy_orders
    except AttributeError:
        return buy_orders


def get_open_sell_orders_list(data):
    sell_orders = []
    try:
        open_orders_page = requests.get(base_path + "orders/sell_orders", headers=data)
        soup = BeautifulSoup(open_orders_page.text, "html.parser")
        orders_list = soup.find("tbody")
        open_order = orders_list.find_all("tr")
        for each in open_order:
            player_dict = {}
            player_name = each.contents[3].text.strip()
            posted_price = each.contents[5].text.strip().replace(",", "")
            order_id = each.get("id")
            player_url = each.find("a")
            player_url = (
                "https://mlb23.theshow.com" + player_url["href"].lstrip().rstrip()
            )
            player_dict["Name"] = player_name
            player_dict["Posted Price"] = posted_price
            player_dict["URL"] = player_url
            player_dict["Order ID"] = order_id
            sell_orders.append(player_dict)

        return sell_orders

    except AttributeError:
        return sell_orders


def get_total_open_orders(data):
    buy_order_list = get_open_buy_orders_list(data)
    sell_order_list = get_open_sell_orders_list(data)
    return buy_order_list + sell_order_list
