# api_qiita_articles.py
from urllib.parse import urlencode

import requests
import streamlit as st

# Qiita APIのベースURL
BASE_URL = "https://qiita.com/api/v2"


def get_qiita_articles(endpoint, params=None, page_size=20, page_num=1):
    """
    Qiita APIから記事を取得するための共通関数。

    指定されたエンドポイントとオプションのパラメータを使用して、
    Qiita APIからデータを取得します。

    Args:
        endpoint (str): APIのエンドポイントを指定します。
        params (dict, optional): クエリパラメータを含む辞書。デフォルトはNoneです。
        page_size (int, optional): １ページのアイテム数（`per_page`パラメータ）
        pane_num (int, optional): ページ番号（`page`パラメータ）

    Returns:
      tuple(list or dict): APIからのレスポンスをJSON形式で返します。
    """

    # `params`引数の指定により、クエリパラメータを変化させる
    if params:
        query_string = urlencode(params)
        page_uri = (
            f"{BASE_URL}/{endpoint}?page={page_num}&per_page={page_size}"
        )
        if query_string == "":
            # uri = page_uri
            uri = f"{page_uri}&query=*"
        else:
            uri = f"{page_uri}&{query_string}"
    else:
        uri = f"{BASE_URL}/{endpoint}"

    print(f"request GET {uri}")
    response = requests.get(uri)

    # Rate-Remainingをヘッダーから取得
    st.session_state.remain_request_rate = int(
        response.headers.get("Rate-Remaining", 0)
    )

    # Total-Countをヘッダーから取得（`items`のみのendpoint時）
    if "items" == endpoint:
        st.session_state.num_search_items = int(
            response.headers.get("Total-Count", 0)
        )
        st.session_state.formated_num_results = format(
            st.session_state.num_search_items, ","
        )

    return response.json()
