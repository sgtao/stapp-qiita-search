import streamlit as st


def main():
    """Streamlitアプリの構築"""
    st.set_page_config(
        page_title="Qiita Search App",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    """
    # 🏠Welcome to Streamlit!

    This application search Qiita articles via Qiita-API-v2.
    enjoy with your heart's desire :heart:.
    """

    st.subheader("Qiita Search App!")
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


if __name__ == "__main__":
    main()
