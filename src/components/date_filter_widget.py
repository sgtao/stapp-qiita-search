# components/date_filter_widget.py
import datetime

import streamlit as st


def date_filter_widget():
    """
    開始日と終了日を選択するためのウィジェットを表示します。
    - 開始日: 現在の月の1日をデフォルト値として設定します。
    - 終了日: 今日の日付をデフォルト値として設定します。
    - 日付は2つのカラムに分けて表示されます。

    Returns:
        tuple: 開始日と終了日を "YYYY-MM-DD" の文字列形式で返します。
        (start_date, end_date)
    """

    # 現在の年月を取得
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)

    # 日付入力を行う
    col_l, col_r = st.columns(2)
    start_date = col_l.date_input("開始日", value=first_day_of_month)
    end_date = col_r.date_input("終了日", value=today)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Expander閉じるときは使用できないの`False`を返す
    return start_date_str, end_date_str
