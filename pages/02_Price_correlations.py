import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
st.set_page_config(page_title="Plotting Demo", layout="wide", page_icon="📈")

def get_data_and_Clean():
    data = pd.read_csv("D:\HoneyTea\HoneyTea_Price_analysis_1.csv", encoding='unicode_escape', index_col=0)
    data = data[data.columns.drop(list(data.filter(regex='Unnamed')))]
    new_prices = data['prices of items on Amazon'].apply(lambda x: x.replace("Â",""))
    data['prices of items on Amazon'] = new_prices
    new_prices_2 = data['prices of items on Amazon'].apply(lambda x: x.replace("Out of Stock, no Prices available",str(np.nan)))
    data['prices of items on Amazon'] = new_prices_2
    prices_non_currency = data['prices of items on Amazon'].str.split("£", expand=True)[1]
    data['prices of items on Amazon'] = prices_non_currency
    data.insert(4, 'currency', "£")
    data['prices of items on Amazon'] = data['prices of items on Amazon'].astype(float)

    ratings = data["star ratings on Amazon"].str.split(expand=True)[0].to_frame()
    ratings = ratings.apply(lambda x: x.replace("Not", str(np.nan)))
    # ratings = ratings.iloc[:,0].astype(float) 
    data.insert(1, 'Item ratings', ratings.iloc[:,0].astype(float).tolist())

    res_list = []
    data_of_interest = data.iloc[:,-4::2]
    for col in data_of_interest:
        test = data_of_interest[col]
        res_list_1 = []
        for row in test:
            if type(row) == float:
                drake = {
                    "number of " + col.split()[-1] + " reviews" : 0
                }
                res_list_1.append(drake)
            else:
                drake = {
                 "number of " + col.split()[-1] + " reviews": len(row.split(",")) 
                }
                res_list_1.append(drake)
        res_list.append(res_list_1)

    return pd.concat([data, pd.concat([pd.DataFrame(a) for a in res_list],axis=1)], axis=1)

data = get_data_and_Clean()

st.header("Observe the correlations between prices and other numerical factors") 
scatter_cols = st.columns(2)

with scatter_cols[0]:

    data_Types = data.dtypes.to_frame()
    data_Types_ = data_Types[(data_Types[0]== "float64") | (data_Types[0] == "int64")]
    data_with_desired_types = data[data_Types_.index.tolist()]

    # st.write(data_with_desired_types)
    scale_standard = StandardScaler()
    scaled_res = scale_standard.fit_transform(data_with_desired_types)
    data_f = pd.DataFrame(scaled_res, columns=data_with_desired_types.columns)
    # st.write(data_f)

    if "scatter_plot_load" not in st.session_state:
        st.session_state["scatter_plot_load"] = False

    def col_scatter_submit():
        st.session_state["scatter_plot_load"] = True

    with st.form("scatter_chart"):
        st.selectbox("xAxis", options=["prices of items on Amazon"], key="xAxis_")
        st.selectbox("yAxis", options=data_Types_.index.tolist(), index=1, key="yAxis_")
        st.form_submit_button("Submit", on_click=col_scatter_submit)

    if st.session_state["scatter_plot_load"] == False or st.session_state['yAxis_'] == "" or st.session_state["xAxis_"] == "":
        st.info("Please fill in the above to view the results")
    else:
        st.radio(label="Data scale", options=["Original", "Normalised"], key="normalised_or_not", horizontal=True, help="Normalised data can help to compare data that are of different units. grams with prices for example which allows you to compare two factors on an apples to apples basis")
        if st.session_state["normalised_or_not"] == "Normalised":
            fig = px.scatter(data_f, x=st.session_state['xAxis_'], y=st.session_state['yAxis_'], color=st.session_state['xAxis_']) 
        else:
            fig = px.scatter(data, x=st.session_state['xAxis_'], y=st.session_state['yAxis_'], color=st.session_state['xAxis_']) 
        # fig = px.scatter(data, x=st.session_state['xAxis_'], y=st.session_state['yAxis_'])
        st.plotly_chart(fig, use_container_width=True)

    

with scatter_cols[1]:

    data_Types = data.dtypes.to_frame()
    data_Types_ = data_Types[(data_Types[0]== "float64") | (data_Types[0] == "int64")]
    data_with_desired_types = data[data_Types_.index.tolist()]

    # st.write(data_with_desired_types)
    scale_standard = StandardScaler()
    scaled_res = scale_standard.fit_transform(data_with_desired_types)
    data_f = pd.DataFrame(scaled_res, columns=data_with_desired_types.columns)
    # st.write(data_f)

    if "heatmap_plot_load" not in st.session_state:
        st.session_state["heatmap_plot_load"] = False

    def col_heatmap_submit():
        st.session_state["heatmap_plot_load"] = True
    

    with st.form("Heatmap chart"):
        st.multiselect("Measure correlations", default=["prices of items on Amazon"], options=data_Types_.index.tolist(), key="heatmap")
        # st.selectbox("yAxis", options=data_Types_.index.tolist())
        st.form_submit_button("Submit", on_click=col_heatmap_submit)

        if st.session_state["heatmap_plot_load"] == False or st.session_state['heatmap'] == "":
            st.info("Please fill in the above to view")
        else:
           
            fig = px.imshow(round(data_f[st.session_state['heatmap']].corr(),3), text_auto=True)
            st.plotly_chart(fig, use_container_width=True)



# st.write(px.data.medals_wide(indexed=True))
# st.write(data_f[st.session_state['heatmap']].corr())
