# pages/13_searched_archive_access.py
import streamlit as st
import os
import json

from components.qiita_item import qiita_item


def _check_selected_file(file_name=None):
    """JSONファイルがリストか単体アイテムかで表示を変えるため、
    ファイル名のキーワードを確認
    """
    if file_name is None:
        return None

    # 拡張子が`.json`であること
    if not file_name.endswith(".json"):
        return None

    # ファイル名に`item`が含まれてる場合、item-dataを応答
    if "item" in file_name:
        return "item-data"

    # ファイル名に`latest`か`searched`が含まれてる場合、list-dataを応答
    if "latest" in file_name or "searched" in file_name:
        return "list-data"

    # その他の場合はNoneを返す
    return None


def list_temporary_files():
    """
    保存された一時ファイルの一覧を表示し、選択されたファイルを読み込む
    Returns:
        tuple:
            - file_path (str or None): 選択されたファイルのパス。
              ファイルが選択されていない場合はNone。
            - file_type (str or None): 読み込んだファイルのタイプ。
              "item-data" または "list-data"。該当ない場合はNone。
    """
    if "temp_dir_path" in st.session_state:
        temp_dir = st.session_state.temp_dir_path
        files = os.listdir(temp_dir)
        if files:
            selected_file = st.selectbox("保存されたファイル一覧", files)
            file_type = _check_selected_file(selected_file)
            if file_type is None:
                st.error("選択したファイルは有効な形式ではありません")
            file_path = os.path.join(temp_dir, selected_file)
            return (file_path, file_type)
        else:
            st.warning("保存されたファイルがありません")
    else:
        st.warning("一時ファイルが保存されていません")

    return (None, None)


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

    st.title("📂Searched Archive Access")
    st.write("一度、検索した記事内容を再度表示します")

    # 一時ファイルの表示
    st.subheader("保存されたファイルの一覧")
    selected_file_path, file_type = list_temporary_files()
    if "shown_file_path" not in st.session_state:
        st.session_state.shown_file_path = ""

    load_btn_label = "ファイルを読み込む"
    if file_type is not None:
        if st.button(load_btn_label):
            with open(selected_file_path, "r") as f:
                articles = json.load(f)
                st.session_state.loaded_articles = articles
            st.success(f"{selected_file_path} を読み込みました")
            st.session_state.shown_file_path = selected_file_path

    st.subheader("読み込んだ記事の表示")
    if st.session_state.shown_file_path == selected_file_path:
        display_loaded_articles(file_type)
    else:
        st.info(f"「{load_btn_label}」をクリックしてください。")


if __name__ == "__main__":
    main()
