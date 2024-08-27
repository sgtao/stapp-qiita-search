# components/list_temporary_files.py
import os

import streamlit as st


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
