# -*- coding: utf-8 -*-

"""
File: utils.py
Author: Dartrisen
Description: some utils for the Groq API.
"""
import random

import requests

from .constants import USER_AGENTS


def get_random_user_agent(user_agent: str = None) -> str:
    return user_agent if user_agent else random.choice(USER_AGENTS)


def get_anon_token(headers: dict) -> str:
    response = requests.get(
        "https://api.groq.com/v1/auth/anon_token",
        headers=headers,
    )
    return response.json()["access_token"]


def create_headers(user_agent: str) -> dict:
    return {
        "Host": "api.groq.com",
        "Connection": "keep-alive",
        "User-Agent": user_agent,
        "Accept": "*/*",
        "Origin": "https://groq.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://groq.com/",
        "Accept-Language": "en-US,en;q=0.9",
    }
