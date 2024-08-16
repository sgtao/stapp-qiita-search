# pages/11_qiita-article-search.py
import datetime

import streamlit as st

from functions.api_qiita_articles import get_qiita_articles
from components.qiita_item import qiita_item


def date_filter_widget():
    """
    開始日と終了日を選択するためのウィジェットを表示します。
    - 開始日: 現在の月の1日をデフォルト値として設定します。
    - 終了日: 今日の日付をデフォルト値として設定します。
    - 日付は2つのカラムに分けて表示されます。

    Returns:
        tuple: 開始日と終了日を "YYYY-MM-DD" の文字列形式で返します。
        (start_date, end_date)
    """

    # 現在の年月を取得
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)

    # 日付入力を行う
    col_l, col_r = st.columns(2)
    start_date = col_l.date_input("開始日", value=first_day_of_month)
    end_date = col_r.date_input("終了日", value=today)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Expander閉じるときは使用できないの`False`を返す
    return start_date_str, end_date_str


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

    # サイドバーにメニューを配置
    st.title("Qiita Article Search")
    # st.subheader(f"selected menu: {selected_menu}")
    st.write(
        "記事の閲覧は、記事IDをitem-viewerのサイドメニュに貼り付けてください"
    )
    st.page_link(
        "pages/12_qiita_item_viewer.py", label="item_viewer", icon="📕"
    )

    # 最新記事の表示
    if selected_menu == "最新記事一覧":
        st.subheader("最新記事一覧")
        if st.button("表示・更新"):
            st.session_state.latest_articles = get_qiita_articles("items")

        if "latest_articles" in st.session_state:
            for article in st.session_state.latest_articles:
                qiita_item(article, id=article["id"])

    # キーワード検索（期間なし）
    elif selected_menu == "キーワード検索（期間なし）":
        st.subheader("キーワード検索")
        keyword = st.text_input("キーワードを入力してください")
        if st.button("検索"):
            st.write(f"query_word: {keyword}")
            st.session_state.search_results = get_qiita_articles(
                "items", params={"query": keyword}
            )

        if "search_results" in st.session_state:
            for article in st.session_state.search_results:
                qiita_item(article, id=article["id"])

    # キーワード検索（期間検索なし）
    elif selected_menu == "キーワード検索（期間検索）":
        start_date, end_date = date_filter_widget()
        keyword = st.text_input("キーワードを入力してください")
        if st.button("検索"):
            st.write(start_date)
            st.write(end_date)
            query_word = (
                keyword + " created:>" + start_date + " created:<" + end_date
            )

            st.write(f"query_word: {query_word}")
            st.session_state.period_results = get_qiita_articles(
                "items",
                params={"query": query_word},
            )

        if "period_results" in st.session_state:
            for article in st.session_state.period_results:
                qiita_item(article, id=article["id"])


if __name__ == "__main__":
    main()
