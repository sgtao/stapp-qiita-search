# pages/13_searched_archive_access.py
import json

import streamlit as st

from components.qiita_item import qiita_item
from components.list_temporary_files import list_temporary_files


def display_loaded_articles(file_type="item-data"):
    """読み込んだ記事を表示する"""
    if "loaded_articles" in st.session_state:
        if file_type == "item-data":
            article = st.session_state.loaded_articles
            qiita_item(article, id=article["id"], article_body=article["body"])
        elif file_type == "list-data":
            articles = st.session_state.loaded_articles
            for article in articles:
                qiita_item(article, id=article["id"])
        else:
            st.info("表示形式をサポートしていません")


def main():
    st.set_page_config(
        page_title="Searched Archive Access",
        page_icon="📂",
        layout="wide",
    )

    # メイン画面
    st.page_link("main.py", label="toHome", icon="🏠")
    st.title("📂Searched Archive Access")
    st.write("一度、検索した記事内容を再度表示します")

    # 一時ファイルの表示
    st.subheader("保存されたファイルの一覧")
    selected_file_path, file_type = list_temporary_files()
    if "shown_file_path" not in st.session_state:
        st.session_state.shown_file_path = ""
        st.session_state.action_message = ""

    load_btn_label = "ファイルを読み込む"
    download_btn_label = "ダウンロードする"
    if file_type is not None:
        col1, col2 = st.columns(2)

        with col1:
            if st.button(load_btn_label):
                with open(selected_file_path, "r") as f:
                    articles = json.load(f)
                    st.session_state.loaded_articles = articles
                st.session_state.shown_file_path = selected_file_path
                st.session_state.action_message = (
                    f"{selected_file_path} を読み込みました"
                )

        with col2:
            with open(selected_file_path, "r") as f:
                file_content = f.read()
            if st.download_button(
                label=download_btn_label,
                data=file_content,
                file_name=selected_file_path.split("/")[-1],
                mime="application/json",
            ):
                st.session_state.shown_file_path = ""
                st.session_state.action_message = (
                    f"{selected_file_path} をダウンロードしました"
                )

        if st.session_state.action_message != "":
            st.success(st.session_state.action_message)

    st.subheader("読み込んだ記事の表示")
    if st.session_state.shown_file_path == selected_file_path:
        display_loaded_articles(file_type)
    else:
        st.info(f"「{load_btn_label}」をクリックしてください。")


if __name__ == "__main__":
    main()
