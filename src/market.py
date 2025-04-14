import requests
from time import sleep


class Market:
    def __init__(self, root_path, api_url, api_mapper):
        self.root_path = root_path
        self.api_url = api_url
        self.api_mapper = api_mapper
        self.listings = []

    def fetch_listings(self):
        total_pages = self._fetch_total_pages()
        for page in range(1, total_pages + 1):
            self.api_mapper.params["page"] = page
            updated_page_url = self.api_mapper.get_api_url()
            self._process_market_page(updated_page_url)

        return self._sort_by_profit(self.listings)

    def _fetch_total_pages(self):
        listings_json = requests.get(self.api_url).json()
        self.total_pages_found = listings_json["total_pages"]

    def _process_market_page(self, api_link):
        results_metadata = requests.get(api_link).json()
        master_listings = results_metadata["listings"]

        for listing in master_listings:
            player_data = self._extract_listing_data(listing)
            if player_data:
                self.listings.append(player_data)

    def _extract_listing_data(self, player):
        try:
            request_name = player["listing_name"]
            buy_amount = int(player["best_buy_price"])
            sell_amount = int(player["best_sell_price"])
            profit = int(sell_amount * 0.9) - buy_amount
            uuid = player["item"]["uuid"]
            url = f"{self.root_path}/items/{uuid}"
            # sellable = getTotalSellable(url, self.headers)

            return {
                "player name": request_name,
                "buy amount": buy_amount,
                "sell amount": sell_amount,
                "profit": profit,
                "URL": url,
                # "sellable": sellable,
            }
        except Exception as e:
            print(f"Error extracting listing: {e}")
            return None

    def _sort_by_profit(self, listings):
        return sorted(listings, key=lambda x: x["profit"], reverse=True)
