from typing import Final

ERROR_SOUND_PATH: Final[str] = "error_sound.mp3"
GET_REQUEST_HEADERS_PATH: Final[str] = "get_request_headers.json"
POST_REQUEST_HEADERS_PATH: Final[str] = "post_request_headers.json"

BASE_API_PATH = "https://mlb25.theshow.com/apis/listings.json"
SINGLE_ITEM_LISTING_API_PATH = "https://mlb25.theshow.com/apis/listing.json"
ROOT_PATH: Final[str] = "https://mlb25.theshow.com"
COMMUNITY_MARKET_PATH: Final[str] = "https://mlb25.theshow.com/community_market"  # noqa: E501
COMPLETED_ORDERS_PATH: Final[str] = "https://mlb25.theshow.com/orders/completed_orders"  # noqa: E501
OPEN_BUY_ORDERS_PATH: Final[str] = "https://mlb25.theshow.com/orders/buy_orders"
OPEN_SELL_ORDERS_PATH: Final[str] = "https://mlb25.theshow.com/orders/sell_orders"

BUY_ORDER_OVERBID: Final[int] = 5
SELL_ORDER_OVERBID: Final[int] = 5
