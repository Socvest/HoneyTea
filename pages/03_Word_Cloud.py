import streamlit as st

st.set_page_config(page_title="Word Cloud", layout="wide",)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.header("Coming soon...")
st.subheader("Observe the predominant words previous users of existing drinks use to describe prices of their products")
