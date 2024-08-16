# api_qiita_articles.py
from urllib.parse import urlencode

import requests

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
        list or dict: APIからのレスポンスをJSON形式で返します。
    """
    if params:
        query_string = urlencode(params)
        url = f"{BASE_URL}/{endpoint}?{query_string}"
    else:
        url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    return response.json()
