# pages/14_uploaded_file_viewer.py
# pages/13_searched_archive_access.py
import json
import streamlit as st
from components.qiita_item import qiita_item

# from components.list_temporary_files import list_temporary_files


def determine_file_type(uploaded_articles):
    """アップロードされた記事のタイプを決定する"""
    if isinstance(uploaded_articles, list):
        return "list-data"
    elif isinstance(uploaded_articles, dict):
        return "item-data"
    return None


def display_loaded_articles(file_type="item-data"):
    """読み込んだ記事を表示する"""
    if "loaded_articles" in st.session_state:
        if file_type == "item-data":
            article = st.session_state.loaded_articles
            qiita_item(article, id=article["id"], article_body=article["body"])
        elif file_type == "list-data":
            articles = st.session_state.loaded_articles
            article_list = []
            for article in articles:
                # 記事タイトルをリンクとして表示n
                # with st.expander(f"{article['title']}"):
                #     st.markdown(f"[{article['title']}]({article['url']})")
                #     qiita_item(
                #         article,
                #         id=article["id"], article_body=article["body"]
                #     )
                article_list.append({article["title"]})
            article_selected = st.radio(
                "記事一覧:",
                article_list,
            )
            st.write(f"selected_item is {article_selected}")
        else:
            st.info("表示形式をサポートしていません")


def main():
    st.set_page_config(
        page_title="Uploaded Article Viewer",
        page_icon="🚀",
        layout="wide",
    )

    # メイン画面
    st.page_link("main.py", label="toHome", icon="🏠")
    st.title("🚀Uploaded Article Viewer")
    st.write("アップロードした記事内容を表示します")

    uploaded_file = st.file_uploader("JSONファイルをアップロード", type="json")
    if uploaded_file is not None:
        try:
            uploaded_articles = json.load(uploaded_file)
            st.session_state.loaded_articles = uploaded_articles
            st.success("ファイルを読み込みました")
            # st.json(uploaded_articles)  # JSON形式で表示
        except json.JSONDecodeError:
            st.error("アップロードファイルは有効なJSONではありません")

    st.subheader("アップロードした記事の表示")
    if "loaded_articles" in st.session_state:
        # ファイルタイプを決定
        file_type = determine_file_type(st.session_state.loaded_articles)
        # アップロードした内容を表示
        display_loaded_articles(file_type)
    else:
        st.info("ファイルをアップロードしてください。")


if __name__ == "__main__":
    main()
