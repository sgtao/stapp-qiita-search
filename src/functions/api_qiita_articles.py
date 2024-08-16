# api_qiita_articles.py
from urllib.parse import urlencode

import requests
import streamlit as st

# Qiita APIのベースURL
BASE_URL = "https://qiita.com/api/v2"


def get_qiita_articles(endpoint, params=None):
    """
    Qiita APIから記事を取得するための共通関数。

    指定されたエンドポイントとオプションのパラメータを使用して、
    Qiita APIからデータを取得します。

    Args:
        endpoint (str): APIのエンドポイントを指定します。
        params (dict, optional): クエリパラメータを含む辞書。デフォルトはNoneです。

    Returns:
      tuple(list or dict): APIからのレスポンスをJSON形式で返します。
    """
    if params:
        query_string = urlencode(params)
        url = f"{BASE_URL}/{endpoint}?{query_string}"
    else:
        url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)

    # Rate-Remainingをヘッダーから取得
    st.session_state.remain_request_rate = int(
        response.headers.get("Rate-Remaining", 0)
    )

    return response.json()
