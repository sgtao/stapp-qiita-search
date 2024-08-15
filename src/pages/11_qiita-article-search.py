# pages/11_qiita-article-search.py
from urllib.parse import urlencode

import streamlit as st
import requests

# Qiita APIのベースURL
BASE_URL = "https://qiita.com/api/v2"


# 共通のAPIリクエスト関数
def get_qiita_articles(endpoint, params=None):
    if params:
        query_string = urlencode(params)
        url = f"{BASE_URL}/{endpoint}?{query_string}"
    else:
        url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    return response.json()


# Streamlitアプリの構築
def main():
    st.title("Qiita Article Search App")

    selected_menu = st.radio(
        "Pick one:", ["最新記事一覧", "キーワード検索", "記事ID指定表示"]
    )
    st.subheader(f"selected menu: {selected_menu}")

    # 最新記事の表示
    if selected_menu == "最新記事一覧":
        st.header("最新記事一覧")
        latest_articles = get_qiita_articles("items")
        for article in latest_articles:
            st.subheader(article["title"])
            st.code(article["id"])
            st.write(article["url"])

    # キーワード検索
    elif selected_menu == "キーワード検索":
        st.header("キーワード検索")
        keyword = st.text_input("キーワードを入力してください")
        if st.button("検索"):
            search_results = get_qiita_articles(
                "items", params={"query": keyword}
            )
            for article in search_results:
                st.subheader(article["title"])
                st.code(article["id"])
                st.write(article["url"])

    # 記事ID指定表示
    elif selected_menu == "記事ID指定表示":
        st.header("記事ID指定表示")
        item_id = st.text_input("記事IDを入力してください")
        if st.button("表示"):
            article = get_qiita_articles(f"items/{item_id}")
            if article:
                st.subheader(article["title"])
                st.write(article["url"])
                st.write(article["body"])


if __name__ == "__main__":
    main()
