import streamlit as st

"""
# Welcome to Streamlit!

Edit `/src` and `/tests` to customize this app to your heart's desire :heart:.
"""

st.subheader("Qiita Article Search App!")
# サイドバーのページに移動
st.page_link(
    "pages/11_qiita_article_search.py",
    label="Qiita Article Search",
    icon="🔍",
)
st.page_link(
    "pages/12_qiita_item_viewer.py",
    label="Qiita Article Item Viewer",
    icon="📕",
)
