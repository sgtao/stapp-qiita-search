# components/display_remain_rate.py
import streamlit as st


def display_remain_rate(label="リクエスト可能数："):
    """
    Qiita APIの残りリクエスト可能数を表示するためのコンポーネント。
    セッションステートに保存された残りのリクエスト可能数を表示し、
    その数が0より大きいかどうかを返します。

    Args:
        label (str): メトリックのラベルを指定します。デフォルトは"リクエスト可能数："です。

    Returns:
        bool: 残りのリクエスト可能数が0より大きければTrueを返します。
    """

    # 可能数を初期化
    if "remain_request_rate" not in st.session_state:
        st.session_state.remain_request_rate = 60

    st.metric(label=label, value=st.session_state.remain_request_rate)

    return st.session_state.remain_request_rate > 0
