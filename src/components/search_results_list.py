# search_results_list.py
import streamlit as st

from components.qiita_item import qiita_item


def search_results_list():
    if "query_word" in st.session_state:
        st.write(f"query_word: {st.session_state.query_word}")

    if "search_results" in st.session_state:
        st.write(f"検索結果: {st.session_state.formated_num_results} 件")
        st.write()
        for article in st.session_state.search_results:
            qiita_item(article, id=article["id"])
