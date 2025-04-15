from urllib.parse import urlparse, parse_qs, urlencode


class APIMapper:
    def __init__(self, base_api_path, card_series_link, team_id_map):
        self.base_api_path = base_api_path
        self.card_series_link = card_series_link
        self.team_id_map = team_id_map
        self.params = {"page": 1}
        self._parse_web_url()

    def _parse_web_url(self):
        parsed_url = urlparse(self.card_series_link)
        query_params = parse_qs(parsed_url.query)

        for web_key, values in query_params.items():
            web_key = web_key.split(";")[1]
            value = values[0] if values else None

            if web_key == "team_id":
                web_key = "team"
                team_id = int(value)
                if team_id in self.team_id_map:
                    self.params[web_key] = self.team_id_map[team_id]
            elif web_key == "max_best_buy_price":
                web_key = "max_best_sell_price"
                self.params[web_key] = value
            elif web_key == "min_best_buy_price":
                web_key = "min_best_sell_price"
                self.params[web_key] = value
            # CAN SKIP ADDING SUBDOMAIN TO API URL AS THAT IS NOT NEEDED IN API CALL
            elif web_key == "subdomain":
                continue
            else:
                self.params[web_key] = value

    def get_api_url(self) -> str:
        """
        Return the full API URL with current parameters.
        """
        print(f"{self.base_api_path}?{urlencode(self.params)}")
        return f"{self.base_api_path}?{urlencode(self.params)}"
