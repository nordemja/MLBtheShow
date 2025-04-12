import requests
from bs4 import BeautifulSoup
from time import sleep


class Market:
    def __init__(
        self, community_market_path, card_series_link, card_series_filter, headers
    ):
        self.community_market_path = community_market_path
        self.card_series_link = card_series_link
        self.card_series_filter = card_series_filter
        self.headers = headers
        self.total_pages_found = 0
        self.listings = []

    def fetch_total_pages(self):
        card_series = requests.get(self.card_series_link, headers=self.headers)
        soup = BeautifulSoup(card_series.text, "html.parser")
        total_pages_found = int(soup.find("h3").text.strip()[-1])
        self.total_pages_found = total_pages_found

    def fetch_listings(self):
        for page in range(1, self.total_pages_found + 1):
            page_link = (
                f"{self.community_market_path}?page={page}&{self.card_series_filter}"
            )
            self._process_market_page(page_link)

        return self._sort_by_profit(self.listings)

    def _process_market_page(self, page_link):
        response = requests.get(page_link, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find("tbody").find_all("tr")

        for row in rows:
            listing = self._extract_listing_data(row)
            if listing:
                self.listings.append(listing)

    # THIS METHOD IS BUGGY AND DOES NOT WORK PROPERY RN :(
    def _extract_listing_data(self, row):
        try:
            request_name = row.contents[5].text.strip()
            buy_amount = int(row.contents[11].text.strip())
            sell_amount = int(row.contents[9].text.strip())
            profit = int(sell_amount * 0.9) - buy_amount
            url_suffix = row.find("a")["href"].strip().lstrip().rstrip("fave")
            url = base_path + url_suffix
            sellable = getTotalSellable(url, self.headers)

            return {
                "player name": request_name,
                "buy amount": buy_amount,
                "sell amount": sell_amount,
                "profit": profit,
                "URL": url,
                "sellable": sellable,
            }
        except Exception as e:
            print(f"Error extracting listing: {e}")
            return None

    def _sort_by_profit(self, listings):
        return sorted(listings, key=lambda x: x["profit"], reverse=True)
