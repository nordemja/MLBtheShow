class BuyOrderSelector:
    """
    Responsible for filtering a list of potential player listings to determine which are
    eligible for new buy orders. This involves checking for duplicate open orders and
    ensuring that the maximum buy and total listing limits are not exceeded.

    Attributes:
        listings (list): List of player listings available for evaluation.
        open_orders (list): Current open buy orders.
        buy_order_length (int): Number of active buy orders.
        total_open_listing_length (int): Combined number of buy and sell orders.
        max_buy_orders (int): Maximum number of buy orders allowed.
        max_total_listings (int): Maximum number of total (buy + sell) listings allowed.

    Methods:
        select_players():
            Filters and returns players eligible for new buy orders based on limits
            and whether an order is already placed.

        _is_order_placed(player_name: str) -> bool:
            Checks whether a buy order for the given player already exists.

        _check_listing_lengths() -> bool:
            Validates whether placing additional orders would exceed configured limits.
    """

    def __init__(
        self, listings, open_orders, buy_order_length, total_open_listing_length
    ):
        """
        Initializes the BuyOrderSelector with player listings, current open orders, and
        the current state of buy and total listings.

        Args:
            listings (list): List of potential player listings to evaluate.
            open_orders (list): List of current open buy orders.
            buy_order_length (int): Current count of open buy orders.
            total_open_listing_length (int): Combined count of all open buy/sell orders.
        """
        self.listings = listings
        self.open_orders = open_orders
        self.buy_order_length = buy_order_length
        self.total_open_listing_length = total_open_listing_length
        self.max_buy_orders = 10
        self.max_total_listings = 25

    def select_players(self):
        """
        Selects a list of players to place buy orders for,
        based on current open orders and listing thresholds.

        Returns:
            list: Filtered list of player listings eligible for new buy orders.
        """
        players_to_buy = []

        for listing in self.listings:
            name = listing["player name"]

            if self._is_order_placed(name):
                print(f"{name} already has an open order and is awaiting fulfillment")
                continue

            if not self._check_listing_lengths():
                print("Maximum listing length reached!")
                print(f"Buy Orders Length: {self.buy_order_length}")
                print(f"Total Buy/Sell Orders Length: {self.total_open_listing_length}")
                break

            print(listing)
            players_to_buy.append(listing)
            self.buy_order_length += 1
            self.total_open_listing_length += 1

        return players_to_buy

    def _is_order_placed(self, player_name):
        """
        Checks if an order for the given player is already placed.

        Args:
            player_name (str): Name of the player.

        Returns:
            bool: True if an order exists, False otherwise.
        """
        return any(order["Name"] == player_name for order in self.open_orders)

    def _check_listing_lengths(self):
        """
        Validates whether more orders can be placed within the allowed limits.

        Returns:
            bool: True if limits are not yet reached, False otherwise.
        """
        return (
            self.buy_order_length < self.max_buy_orders
            and self.total_open_listing_length < self.max_total_listings
        )
