# pages/11_qiita-article-search.py
import streamlit as st

from functions.api_qiita_articles import get_qiita_articles


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
                # 記事タイトルをリンクとして表示
                st.markdown(f"### [{article['title']}]({article['url']})")
                # 記事の基本情報を表示
                user_name = article["user"]["name"]
                user_id = article["user"]["id"]
                group_info = (
                    article["group"]["name"] if article["group"] else "なし"
                )
                group_id = (
                    article["group"]["id"] if article["group"] else "なし"
                )
                info_text = (
                    f"記事ID: {article['id']}, "
                    f"作成日: {article['created_at']}, "
                    f"最終更新日: {article['updated_at']}, "
                    f"作成者: {user_name} (ID: {user_id} ), "
                    f"グループ: {group_info} (ID: {group_id})"
                )
                st.write()
                st.success(info_text)
                # タグリストを作成
                tag_list = ", ".join(tag["name"] for tag in article["tags"])
                st.write()
                st.info(f"タグ: {tag_list}")
                # 記事本文を表示
                st.write(article["body"])


if __name__ == "__main__":
    main()
