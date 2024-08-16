# search_pagination.py
import streamlit as st

from functions.api_qiita_articles import get_qiita_articles


def search_pagination():
    left, medium, right = st.columns(3)
    col1, col2, col3 = medium.columns(3)
    total_pages = int(st.session_state.num_search_items / 20) + 1
    formated_total_pages = format(total_pages, ",")

    if st.session_state.page_num > 1:
        # 前のページ
        if col1.button(label="◀", help="前のページ"):
            st.session_state.page_num = st.session_state.page_num - 1
            st.session_state.search_results = get_qiita_articles(
                "items",
                params={"query": st.session_state.query_word},
                page_num=st.session_state.page_num,
            )
            st.rerun()

    # ページ数表示（現在／総頁）
    col2.write(f"{st.session_state.page_num} / {formated_total_pages}")

    # 次のページ
    if st.session_state.page_num < total_pages:
        if col3.button(label="▶", help="次のページ"):
            st.session_state.page_num = st.session_state.page_num + 1
            st.session_state.search_results = get_qiita_articles(
                "items",
                params={"query": st.session_state.query_word},
                page_num=st.session_state.page_num,
            )
            st.rerun()
