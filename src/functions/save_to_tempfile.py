# functions/save_to_tempfile.py
import datetime
import json
import tempfile
import os

import streamlit as st


def save_to_tempfile(label, articles):
    """記事を一時ファイルに保存する"""
    if "temp_dir_path" not in st.session_state:
        temp_dir = tempfile.mkdtemp()
        st.session_state.temp_dir_path = temp_dir
    temp_dir = st.session_state.temp_dir_path
    now = datetime.datetime.now()
    cur_datetime = now.strftime("%y%m%d-%H%M%S")
    save_file_name = f"{cur_datetime}-{label}.json"
    temp_file_path = os.path.join(temp_dir, save_file_name)
    with open(temp_file_path, "w") as f:
        json.dump(articles, f)

    return temp_file_path


def delete_tempfile(temp_file_path):
    """一時ファイルを削除する"""
    try:
        # delete tempfile
        os.remove(temp_file_path)
    except Exception as e:
        st.error(f"Error deleting temporary file: {e}")
