import streamlit as st
def sidebar():
    with st.sidebar:
        st.markdown(
            "## Анализ сроков строительства\n"
            "1. Добавьте файл \n"
            "2. Выберите объект для анализа📄\n"  # noqa: E501
            "3. Получите анализ рисков\n"
        )