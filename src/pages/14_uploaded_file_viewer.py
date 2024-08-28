# pages/14_uploaded_file_viewer.py
import json
import streamlit as st
from components.qiita_item import qiita_item


def determine_file_type(uploaded_articles):
    """アップロードされた記事のタイプを決定する"""
    if isinstance(uploaded_articles, list):
        return "list-data"
    elif isinstance(uploaded_articles, dict):
        return "item-data"
    return None


def select_item_from_loaded_articles(file_type="item-data"):
    """読み込んだ記事のID選択を表示し、選択された記事IDを返す"""
    article_id_list = []
    article_title_list = []
    articleId_selected = ""
    if "loaded_articles" in st.session_state:
        articles = st.session_state.loaded_articles
        if file_type == "item-data":
            article = st.session_state.loaded_articles
            article_id_list.append(f'{article["id"]}')
            article_title_list.append(f'{article["title"]}')
        elif file_type == "list-data":
            for article in articles:
                article_id_list.append(f'{article["id"]}')
                article_title_list.append(f'{article["title"]}')
        else:
            st.info("表示形式をサポートしていません")

    with st.expander("記事選択"):
        articleId_selected = st.radio(
            label="記事一覧:",
            options=article_id_list,
            format_func=lambda x: article_title_list[article_id_list.index(x)],
        )
    return articleId_selected


def main():
    st.set_page_config(
        page_title="Uploaded Article Viewer",
        page_icon="🚀",
        layout="wide",
    )

    # メイン画面
    st.title("🚀Uploaded Article Viewer")
    st.write("アップロードした記事内容を表示します")

    uploaded_file = st.file_uploader("JSONファイルをアップロード", type="json")
    if uploaded_file is not None:
        try:
            uploaded_articles = json.load(uploaded_file)
            st.session_state.loaded_articles = uploaded_articles
            st.success("ファイルを読み込みました")
        except json.JSONDecodeError:
            st.error("アップロードファイルは有効なJSONではありません")

    st.subheader("アップロードした記事の表示")
    if "loaded_articles" in st.session_state:
        file_type = determine_file_type(st.session_state.loaded_articles)
        article_id = select_item_from_loaded_articles(file_type)
        if article_id:
            st.write(f"選択された記事ID: {article_id}")
            if file_type == "item-data":
                article = st.session_state.loaded_articles
                qiita_item(
                    article, id=article["id"], article_body=article["body"]
                )
            elif file_type == "list-data":
                articles = st.session_state.loaded_articles
                for article in articles:
                    if article["id"] == article_id:
                        qiita_item(
                            article,
                            id=article["id"],
                            article_body=article["body"],
                        )
                        break
    else:
        st.info("ファイルをアップロードしてください。")


if __name__ == "__main__":
    main()
