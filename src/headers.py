import json
import requests
from pathlib import Path


class Headers:
    def __init__(self, headers_path: str):
        self.headers_path = Path(headers_path)
        self.headers = self._load_headers()

    def get_headers(self) -> dict:
        return self.headers

    def update_cookie(self, new_cookie: str):
        self.headers["cookie"] = new_cookie
        self._save_headers()

    def _load_headers(self) -> dict:
        if not self.headers_path.exists():
            raise FileNotFoundError(f"Header file not found: {self.headers_path}")
        with self.headers_path.open("r") as f:
            return json.load(f)

    def _save_headers(self):
        with self.headers_path.open("w") as f:
            json.dump(self.headers, f, indent=4)
