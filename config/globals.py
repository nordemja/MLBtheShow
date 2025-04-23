from typing import Final

ERROR_SOUND_PATH: Final[str] = "error_sound.mp3"
HEADERS_PATH: Final[str] = "headers.json"

BASE_API_PATH = "https://mlb23.theshow.com/apis/listings.json"
SINGLE_ITEM_LISTING_API_PATH = "https://mlb23.theshow.com/apis/listing.json"
ROOT_PATH = "https://mlb23.theshow.com"
COMMUNITY_MARKET_PATH: Final[str] = "https://mlb23.theshow.com/community_market"  # noqa: E501
COMPLETED_ORDERS_PATH: Final[str] = "https://mlb23.theshow.com/orders/completed_orders"  # noqa: E501
OPEN_BUY_ORDERS_PATH: Final[str] = "https://mlb23.theshow.com/orders/buy_orders"
OPEN_SELL_ORDERS_PATH: Final[str] = "https://mlb23.theshow.com/orders/sell_orders"
CAPTCHA_SOLVER_SEND_LINK: Final[str] = f"https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={player_url}&json=1&invisible=1"   # noqa: E501
CAPTCHA_SOLVER_GET_TOKEN_LINK: Final[str] = f"https://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"   # noqa: E501
