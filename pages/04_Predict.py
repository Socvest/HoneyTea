import streamlit as st

st.set_page_config(page_title="Price Prediction", layout="wide")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.header("Coming soon...")
st.subheader("Predict the price of your drink based on certain parameters derived from what is out there in the market")
