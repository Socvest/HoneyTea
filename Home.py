import streamlit as st

st.set_page_config(layout="wide")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.header("HoneyTea Business Development")
st.write("This is a private app that you can use to build your analysis for the development of the company - later we can build a better one that is privately hosted and designed to do exactly what you want. But this is a quick one.")
