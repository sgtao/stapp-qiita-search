# qiita_item.py
import streamlit as st


def qiita_item(article, id=None, article_body=None):
    # 記事タイトルをリンクとして表示n
    st.markdown(f"### [{article['title']}]({article['url']})")
    # id をコピーボタン付きで表示
    if id is not None:
        col1, col2 = st.columns([1, 2])
        col1.info("記事ID(for copy):")
        col2.code(article["id"])

    with st.expander("show item info.", expanded=True, icon="📌"):
        # 記事の基本情報を表示
        user_name = article["user"]["name"]
        user_id = article["user"]["id"]
        group_info = article["group"]["name"] if article["group"] else "なし"
        group_id = article["group"]["id"] if article["group"] else "なし"
        info_text = (
            f"記事ID: {article['id']}, "
            f"作成日: {article['created_at']}, "
            f"最終更新日: {article['updated_at']}, "
            f"作成者: {user_name} (ID: {user_id} ), "
            f"グループ: {group_info} (ID: {group_id})"
        )
        st.write()
        st.success(info_text)
        # タグリストを作成
        tag_list = " ".join(tag["name"] for tag in article["tags"])
        st.write()
        st.info(f"タグ: {tag_list}")

    if article_body is not None:
        # 記事本文を表示
        st.write(article_body)

    # 区切り線を追加
    st.markdown("---")
