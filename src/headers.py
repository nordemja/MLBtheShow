import json
from pathlib import Path
from typing import Dict
from playsound import playsound


class Headers:
    """
    Manages the loading, updating, and saving of HTTP headers from a JSON file.

    This class is responsible for reading headers from a file, providing access to them,
    and allowing updates, particularly the cookie field, which can be updated or removed.

    Attributes:
        headers_path (Path): Path to the JSON file containing the headers.
        headers (Dict[str, str]): A dictionary holding the loaded headers data.

    Methods:
        get_headers() -> Dict[str, str]:
            Retrieves the current headers dictionary.

        update_cookie(new_cookie: str) -> None:
            Updates the 'cookie' field in the headers with the given value.

        delete_cookie() -> None:
            Removes the 'cookie' field from the headers.

        _load_headers() -> Dict[str, str]:
            Loads the headers from the JSON file.

        _save_headers() -> None:
            Saves the current headers to the JSON file.
    """

    def __init__(self, error_sound_path: str, headers_path: str, browser):
        """
        Initialize the Headers manager.

        Args:
            headers_path (str): Path to the JSON file containing header data.
        """
        self.error_sound_path = error_sound_path
        self.headers_path = Path(headers_path)
        self.browser = browser
        self.headers: Dict[str, str] = self._load_headers()

    def get_headers(self) -> Dict[str, str]:
        """
        Retrieve the current headers.

        Returns:
            Dict[str, str]: The headers dictionary.
        """
        return self.headers

    def update_cookie(self, new_cookie: str) -> None:
        """
        Update the 'cookie' field in the headers.

        Args:
            new_cookie (str): The new cookie string to set.
        """
        print("updating headers....")

        # if first run - then get full auth cookie
        if "cookie" not in self.headers:
            self.headers["cookie"] = new_cookie

        # executed anytime after first run - just update the tsn_session in the cookie field
        else:
            cookies = self.headers["cookie"].split(";")
            new_full_user_cookie = ""
            for i, cookie in enumerate(cookies):
                if "_tsn_session" in cookie:
                    cookies[i] = cookie.split("=")[0] + "=" + new_cookie
                    print(cookies[i])
                new_full_user_cookie += cookies[i] + ";"

            # take the entire string except the last character - this is to avoid getting the trailing semicolon
            new_full_user_cookie = new_full_user_cookie[:-1]
            print(new_full_user_cookie)
            self.headers["cookie"] = new_full_user_cookie

        self._save_headers()

    def get_and_update_new_auth_cookie(self) -> None:
        """
        Use the browser to fetch a new cookie from the given URL and update headers.
        """
        print("Refreshing cookie using browser...")
        playsound(self.error_sound_path)
        old_tsn_session = self.browser.tsn_session
        self.browser.get_cookie_header_from_browser(
            url="https://mlb25.theshow.com/dashboard"
        )
        new_tsn_session = self.browser.tsn_session
        if old_tsn_session != new_tsn_session:
            self.update_cookie(new_cookie=new_tsn_session)
        else:
            print("Failed to retrieve cookie from browser.")

    def delete_cookie(self) -> None:
        """
        Remove the 'cookie' field from the headers.
        """
        print("removing auth cookie from headers.....")
        del self.headers["cookie"]
        self._save_headers()

    def _load_headers(self) -> Dict[str, str]:
        """
        Load headers from the JSON file.

        Returns:
            Dict[str, str]: The loaded headers dictionary.

        Raises:
            FileNotFoundError: If the header file does not exist.
        """
        if not self.headers_path.exists():
            raise FileNotFoundError(f"Header file not found: {self.headers_path}")
        with self.headers_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save_headers(self) -> None:
        """
        Save the current headers to the JSON file.
        """
        with self.headers_path.open("w", encoding="utf-8") as f:
            json.dump(self.headers, f, indent=4)
