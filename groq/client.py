# -*- coding: utf-8 -*-

"""
File: client.py
Author: Dartrisen
Description: unofficial client for the Groq API.
"""
import json
from http.client import IncompleteRead
from time import time
from typing import List, Iterator

import requests

from .models import Chat, Stats
from .utils import get_random_user_agent, get_anon_token, create_headers


class StreamingChat:
    """Live-streaming chat class."""

    def __init__(self, url: str, headers: dict, json_data: dict) -> None:
        self._url = url
        self._headers = headers
        self._json_data = json_data
        self._response = None

    def __enter__(self):
        self._response = requests.post(
            self._url, headers=self._headers, json=self._json_data, stream=True
        )

        # Check if the request was successful before creating the iterator
        if not self._response or self._response.status_code != 200:
            raise Exception(f"Request failed with status code {self._response.status_code}")

        def iterator() -> Iterator[str]:
            try:
                for chunk in self._response.iter_lines(decode_unicode=True):
                    if chunk:
                        loaded = json.loads(chunk)
                        yield loaded.get("result", {}).get("content", "")
            except (TypeError, IncompleteRead) as e:
                print(f"Error while decoding JSON: {e}")
                raise

        return iterator()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._response:
            self._response.close()


# pylint: disable=too-few-public-methods, too-many-arguments
class Client:
    """Client class."""

    BASE_URL = "https://api.groq.com/v1"
    API_URL = f"{BASE_URL}/request_manager/text_completion"

    def __init__(self, proxies: dict = None, user_agent: str = None, retries: int = 0) -> None:
        self._proxies = proxies
        self._user_agent = get_random_user_agent(user_agent)
        self._retries = retries
        self._headers = create_headers(self._user_agent)
        self._auth_token = get_anon_token(self._headers)
        self._headers["authorization"] = f"Bearer {self._auth_token}"
        self._auth_token_last_updated = int(time())

    def create_chat(
            self,
            user_prompt: str,
            model_id: str = "mixtral-8x7b-32768",
            system_prompt: str = "Please try to provide useful, helpful and actionable answers.",
            history: List[str] = None,
            seed: int = 10,
            max_tokens: int = 32768,
            temperature: float = 0.2,
            top_k: int = 40,
            top_p: float = 0.8,
            max_input_tokens: int = 21845
    ) -> Chat:
        if model_id == "llama2-70b-4096":
            max_tokens = min(4096, max_tokens)
            max_input_tokens = min(2730, max_input_tokens)
        if history is None:
            history = []
        json_data = {
            "model_id": model_id,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "history": history,
            "seed": seed,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "max_input_tokens": max_input_tokens,
        }
        response = requests.post(
            self.API_URL,
            headers=self._headers,
            json=json_data,
            proxies=self._proxies,
            timeout=40,
        )
        res = ""
        request_id = None
        stats = Stats(
            time_generated=0, tokens_generated=0, time_processed=0, tokens_processed=0
        )

        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:  # filter out keep-alive new chunks
                try:
                    loaded = json.loads(chunk)

                    if loaded["result"].get("requestId", None):
                        request_id = loaded["result"]["requestId"]

                    if loaded["result"].get("stats", None):
                        stats = Stats(
                            time_generated=loaded["result"]["stats"]["timeGenerated"],
                            tokens_generated=loaded["result"]["stats"][
                                "tokensGenerated"
                            ],
                            time_processed=loaded["result"]["stats"]["timeProcessed"],
                            tokens_processed=loaded["result"]["stats"][
                                "tokensProcessed"
                            ],
                        )

                    res += loaded["result"].get("content", "")
                except json.JSONDecodeError as e:
                    print(f"Error while decoding JSON: {e}")
                    continue

        return Chat(
            content=res,
            request_id=request_id,
            stats=stats,
        )

    def create_streaming_chat(
            self,
            user_prompt: str,
            model_id: str = "mixtral-8x7b-32768",
            system_prompt: str = "Please try to provide useful, helpful and actionable answers.",
            history: List[str] = None,
            seed: int = 10,
            max_tokens: int = 32768,
            temperature: float = 0.2,
            top_k: int = 40,
            top_p: float = 0.8,
            max_input_tokens: int = 21845
    ) -> StreamingChat:
        if model_id == "llama2-70b-4096":
            max_tokens = min(4096, max_tokens)
            max_input_tokens = min(2730, max_input_tokens)
        if history is None:
            history = []
        json_data = {
            "model_id": model_id,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "history": history,
            "seed": seed,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "max_input_tokens": max_input_tokens,
        }
        return StreamingChat(self.API_URL, self._headers, json_data)
