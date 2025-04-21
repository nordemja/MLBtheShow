class OrderChecker:
    def __init(self, single_item_api_path):
        self.single_item_api_path = single_item_api_path
        self.player_list = []

    def check_buy_orders(self, orders: list[dict]):
        for order in orders:
            uuid = order["URL"].split("/")[-1]
            current_buy_price = self._get_current_buy_amount(uuid)
            posted_price = int(order["Posted Price"])

            if posted_price < current_price:

                self.player_list.append(
                    {
                        "player name": order["Name"],
                        "buy amount": current_buy_price,
                        "URL": order["URL"],
                    }
                )

                self._cancel_order(order)
            else:
                print(f"{order['Name']} at {posted_price} is currently best sell price")

        return self.player_list

    def check_sell_orders(self, orders: list[dict]):
        for order in orders:
            uuid = order["URL"].split("/")[-1]
            current_sell_price = self._get_current_sell_amount(uuid)
            posted_price = int(order["Posted Price"])

            if posted_price > current_price:

                self.player_list.append(
                    {
                        "player name": order["Name"],
                        "sell amount": current_sell_price,
                        "URL": order["URL"],
                    }
                )

                self._cancel_order(order=order)

            else:
                print(f"{order['Name']} at {posted_price} is currently best buy price")

        return self.player_list

    def _cancel_order(self, order: dict):
        try:
            print(f"Cancelling order for {order['Name']}")
            self.browser.find_element(
                "xpath",
                f'//*[@id="{order["Order ID"]}"]/td[1]/form/button',
            ).click()
            self.browser.switch_to.alert.accept()

        except Exception as e:
            self._handle_error(f"Failed to cancel order for {order['Name']}", e)

    def _get_current_buy_amount(self, uuid):

        response = requests.get(f"{self.single_item_api_path}?uuid={uuid}").json()
        current_buy_ammount = response["best_buy_price"]
        return int(current_buy_ammount)

    def _get_current_sell_amount(self, uuid):

        response = requests.get(f"{self.single_item_api_path}?uuid={uuid}").json()
        current_sell_ammount = response["best_sell_price"]
        return int(current_sell_ammount)
