# components/show_temporary_message.py
import time

import streamlit as st


def show_temporary_message(message, duration=3):
    """一時的にメッセージを表示する"""
    placeholder = st.empty()
    placeholder.success(message)
    time.sleep(duration)
    placeholder.empty()
