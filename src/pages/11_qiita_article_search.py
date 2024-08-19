# pages/11_qiita-article-search.py
import streamlit as st

from functions.api_qiita_articles import get_qiita_articles
from functions.save_to_tempfile import save_to_tempfile
from components.qiita_item import qiita_item
from components.date_filter_widget import date_filter_widget
from components.display_remain_rate import display_remain_rate
from components.search_results_list import search_results_list
from components.search_pagination import search_pagination
from components.show_temporary_message import show_temporary_message


def main():
    """Streamlitアプリの構築"""
    st.set_page_config(
        page_title="Qiita Article Search",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # サイドバーにメニューを配置
    with st.sidebar:
        selected_menu = st.radio(
            "メニューを選択:",
            [
                "最新記事一覧",
                "キーワード検索（期間なし）",
                "キーワード検索（期間検索）",
            ],
        )
        display_remain_rate(label="検索可能数：")

    # メイン画面
    st.title("🔍Qiita Article Search")
    # st.subheader(f"selected menu: {selected_menu}")
    st.write(
        "記事の閲覧は、記事IDをitem-viewerのサイドメニュに貼り付けてください"
    )
    st.page_link(
        "pages/12_qiita_item_viewer.py", label="item_viewer", icon="📕"
    )

    # 検索結果のアイテム数を初期化
    if "num_search_items" not in st.session_state:
        st.session_state.num_search_items = 0
    if "page_num" not in st.session_state:
        st.session_state.page_num = 1

    # 最新記事の表示
    if selected_menu == "最新記事一覧":
        st.subheader("最新記事一覧")
        if st.button("表示・更新"):
            articles = get_qiita_articles("items")
            st.session_state.temp_file_path = save_to_tempfile(
                "latest", articles
            )
            st.session_state.latest_articles = articles

        if "latest_articles" in st.session_state:
            st.write(
                f"最新 20件 of {st.session_state.formated_num_results} 件"
            )
            show_temporary_message(
                f"Articles saved to: {st.session_state.temp_file_path}"
            )

            for article in st.session_state.latest_articles:
                qiita_item(article, id=article["id"])

    # キーワード検索（期間なし）
    elif selected_menu == "キーワード検索（期間なし）":
        st.subheader("キーワード検索")
        keyword = st.text_input("キーワードを入力してください")
        if st.button("検索"):
            query_word = keyword
            st.session_state.query_word = query_word
            st.session_state.search_results = get_qiita_articles(
                "items", params={"query": query_word}
            )
            st.session_state.page_num = 1
            st.session_state.temp_file_path = save_to_tempfile(
                "searched", st.session_state.search_results
            )
            show_temporary_message(
                f"Articles saved to: {st.session_state.temp_file_path}"
            )

        # 検索結果の表示
        search_results_list()
        # ページネーションの表示
        search_pagination()

    # キーワード検索（期間検索なし）
    elif selected_menu == "キーワード検索（期間検索）":
        start_date, end_date = date_filter_widget()
        keyword = st.text_input("キーワードを入力してください")
        if st.button("検索"):
            # st.write(start_date)
            # st.write(end_date)
            query_word = (
                keyword + " created:>=" + start_date + " created:<=" + end_date
            )

            st.session_state.query_word = query_word
            st.session_state.search_results = get_qiita_articles(
                "items",
                params={"query": query_word},
            )
            st.session_state.page_num = 1
            st.session_state.temp_file_path = save_to_tempfile(
                "periodSrch", st.session_state.search_results
            )
            show_temporary_message(
                f"Articles saved to: {st.session_state.temp_file_path}"
            )

        # 検索結果の表示
        search_results_list()
        # ページネーションの表示
        search_pagination()


if __name__ == "__main__":
    main()
