import json
from typing import Dict
from pathlib import Path

# from playsound import playsound


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

    def __init__(self, error_sound_path: str):
        """
        Initialize the Headers manager.

        Args:
            headers_path (str): Path to the JSON file containing header data.
        """
        self.error_sound_path = error_sound_path

    def get_headers(self, headers_path) -> Dict[str, str]:
        """
        Retrieve the current headers.

        Returns:
            Dict[str, str]: The headers dictionary.
        """
        return self._load_headers(headers_path)

    def _load_headers(self, headers_path) -> Dict[str, str]:
        """
        Load headers from the JSON file.

        Returns:
            Dict[str, str]: The loaded headers dictionary.

        Raises:
            FileNotFoundError: If the header file does not exist.
        """
        headers_path = Path(headers_path)
        if not headers_path.exists():
            raise FileNotFoundError(f"Header file not found: {headers_path}")
        with headers_path.open("r", encoding="utf-8") as f:
            return json.load(f)
