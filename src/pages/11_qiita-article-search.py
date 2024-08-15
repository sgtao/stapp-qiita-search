# pages/11_qiita-article-search.py
from urllib.parse import urlencode

import streamlit as st
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


def main():
    """Streamlitアプリの構築"""

    # サイドバーにメニューを配置
    with st.sidebar:
        selected_menu = st.radio(
            "メニューを選択:",
            ["最新記事一覧", "キーワード検索", "記事ID指定表示"],
        )

    # サイドバーにメニューを配置
    st.title("Qiita Article Search App")
    # st.subheader(f"selected menu: {selected_menu}")

    # 最新記事の表示
    if selected_menu == "最新記事一覧":
        st.subheader("最新記事一覧")
        if st.button("表示・更新"):
            st.session_state.latest_articles = get_qiita_articles("items")

        if "latest_articles" in st.session_state:
            for article in st.session_state.latest_articles:
                st.subheader(article["title"])
                st.code(article["id"])
                st.write(article["url"])

    # キーワード検索
    elif selected_menu == "キーワード検索":
        st.subheader("キーワード検索")
        keyword = st.text_input("キーワードを入力してください")
        if st.button("検索"):
            st.session_state.search_results = get_qiita_articles(
                "items", params={"query": keyword}
            )

        if "search_results" in st.session_state:
            for article in st.session_state.search_results:
                st.subheader(article["title"])
                st.code(article["id"])
                st.write(article["url"])

    # 記事ID指定表示
    elif selected_menu == "記事ID指定表示":
        st.subheader("記事ID指定表示")
        if "shown_item_id" not in st.session_state:
            st.session_state.shown_item_id = ""

        item_id = st.text_input(
            label="記事IDを入力してください",
            value=st.session_state.shown_item_id,
        )
        if item_id != st.session_state.shown_item_id:
            st.session_state.shown_article = get_qiita_articles(
                f"items/{item_id}"
            )
            st.session_state.shown_item_id = item_id

        if "shown_article" in st.session_state:
            article = st.session_state.shown_article
            if article:
                st.subheader(article["title"])
                st.write(f"ID: {article['id']}")
                st.write(article["url"])
                st.write(article["body"])


if __name__ == "__main__":
    main()
