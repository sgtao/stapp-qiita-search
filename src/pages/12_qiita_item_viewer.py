# pages/12_qiita-item-viewer.py
import streamlit as st

from functions.api_qiita_articles import get_qiita_articles
from components.qiita_item import qiita_item
from components.display_remain_rate import display_remain_rate


def main():
    """Streamlitアプリの構築"""
    st.set_page_config(
        page_title="Qiita Article Item Viewer",
        page_icon="📕",
        layout="wide",
        initial_sidebar_state="expanded",
    )

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
        display_remain_rate(label="表示可能数：")

    # メイン画面
    st.title("📕Qiita Article Item Viewer")
    # st.subheader(f"article id: {st.session_state.shown_item_id}")
    st.write(
        "記事の閲覧は、記事IDをitem-viewerのサイドメニュに貼り付けてください"
    )

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
