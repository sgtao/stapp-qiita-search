# pages/11_qiita-article-search.py
import streamlit as st
import requests

# Qiita APIのベースURL
BASE_URL = "https://qiita.com/api/v2"


# 最新記事を取得する関数
def get_latest_articles():
    response = requests.get(f"{BASE_URL}/items")
    return response.json()


# キーワードで記事を検索する関数
def search_articles_by_keyword(keyword):
    response = requests.get(f"{BASE_URL}/items", params={"query": keyword})
    return response.json()


# 記事IDで記事を取得する関数
def get_article_by_id(item_id):
    response = requests.get(f"{BASE_URL}/items/{item_id}")
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
        latest_articles = get_latest_articles()
        for article in latest_articles:
            st.subheader(article["title"])
            st.code(article["id"])
            st.write(article["url"])

    # キーワード検索
    elif selected_menu == "キーワード検索":
        st.header("キーワード検索")
        keyword = st.text_input("キーワードを入力してください")
        if st.button("検索"):
            search_results = search_articles_by_keyword(keyword)
            for article in search_results:
                st.subheader(article["title"])
                st.code(article["id"])
                st.write(article["url"])

    # 記事ID指定表示
    elif selected_menu == "記事ID指定表示":
        st.header("記事ID指定表示")
        item_id = st.text_input("記事IDを入力してください")
        if st.button("表示"):
            article = get_article_by_id(item_id)
            if article:
                st.subheader(article["title"])
                st.write(article["url"])
                st.write(article["body"])


if __name__ == "__main__":
    main()
