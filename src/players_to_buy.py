class PlayersToBuy:
    def __init__(
        self,
        listings,
        open_orders,
        buy_order_length,
        total_open_listing_length,
        max_buy_orders=10,
        max_total_listings=25,
    ):
        self.listings = listings
        self.open_orders = open_orders
        self.buy_order_length = buy_order_length
        self.total_open_listing_length = total_open_listing_length
        self.max_buy_orders = max_buy_orders
        self.max_total_listings = max_total_listings
        self.selected_players = []

    def select_players(self):
        for listing in self.listings:
            name = listing["player name"]

            if self._is_order_placed(name):
                print(f"{name} already owned and ready to be sold")
                continue

            # if self._is_sellable(listing):
            #     print(f"{name} is already owned and ready to be sold")

            if not self._check_listing_lengths():
                print("Maximum listing length reached!")
                print(f"Buy Orders Length: {self.buy_order_length}")
                print(f"Total Buy/Sell Orders Length: {self.total_open_listing_length}")
                break

            print(listing)
            self.selected_players.append(listing)
            self.buy_order_length += 1
            self.total_open_listing_length += 1

        return self.select_players

    # def _is_sellable(self, listing):
    #     return listing.get("sellable", 0) > 0

    def _is_order_placed(self, player_name):
        return any(order["Name"] == player_name for order in self.open_orders)

    def _check_listing_lengths(self):
        return (
            self.buy_order_length < self.max_buy_orders
            and self.total_open_listing_length < self.max_total_listings
        )
