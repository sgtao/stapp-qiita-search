# pages/11_qiita-article-search.py
import streamlit as st

from functions.api_qiita_articles import get_qiita_articles
from components.qiita_item import qiita_item


def main():
    """Streamlitアプリの構築"""

    # サイドバーにメニューを配置
    with st.sidebar:
        selected_menu = st.radio(
            "メニューを選択:",
            ["最新記事一覧", "キーワード検索"],
        )

    # サイドバーにメニューを配置
    st.title("Qiita Article Search App")
    # st.subheader(f"selected menu: {selected_menu}")
    st.write(
        "記事の閲覧は、記事IDをitem-viewerのサイドメニュに貼り付けてください"
    )
    st.page_link(
        "pages/12_qiita-item-viewer.py", label="item-viewer", icon="📕"
    )

    # 最新記事の表示
    if selected_menu == "最新記事一覧":
        st.subheader("最新記事一覧")
        if st.button("表示・更新"):
            st.session_state.latest_articles = get_qiita_articles("items")

        if "latest_articles" in st.session_state:
            for article in st.session_state.latest_articles:
                qiita_item(article, id=article["id"])

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
                qiita_item(article, id=article["id"])


if __name__ == "__main__":
    main()
