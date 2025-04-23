import json
from pathlib import Path
from typing import Dict


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

    def __init__(self, headers_path: str):
        """
        Initialize the Headers manager.

        Args:
            headers_path (str): Path to the JSON file containing header data.
        """
        self.headers_path = Path(headers_path)
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
        self.headers["cookie"] = new_cookie
        self._save_headers()

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
