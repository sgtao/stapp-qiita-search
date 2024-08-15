# pages/12_qiita-item-viewer.py
import streamlit as st

from functions.api_qiita_articles import get_qiita_articles
from components.qiita_item import qiita_item


def main():
    """Streamlitアプリの構築"""

    # サイドバーにメニューを配置
    with st.sidebar:
        st.subheader("記事ID指定表示")
        if "shown_item_id" not in st.session_state:
            st.session_state.shown_item_id = ""

        item_id = st.text_input(
            label="記事ID",
            value=st.session_state.shown_item_id,
            placeholder="記事IDを入力してください",
        )

    # サイドバーにメニューを配置
    st.title("Qiita Article Item Viewer")
    # st.subheader(f"article id: {st.session_state.shown_item_id}")

    # 区切り線を追加
    st.markdown("---")

    # 記事ID指定表示
    if item_id != st.session_state.shown_item_id:
        st.session_state.shown_item_id = item_id
        st.session_state.shown_article = get_qiita_articles(f"items/{item_id}")

    if "shown_article" in st.session_state:
        article = st.session_state.shown_article
        if article:
            qiita_item(article, article_body=article["body"])


if __name__ == "__main__":
    main()
