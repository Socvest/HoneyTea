import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
st.set_page_config(page_title="Price Trends", layout="wide", page_icon="📈")

def get_data_and_Clean():
    data = pd.read_csv("HoneyTea_Price_analysis_1.csv", encoding='unicode_escape', index_col=0)
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

# main_Cols = st.columns(2)

def test(
    # colNumber=0,
    load_session_state="column_1_submit",
    form_session_state="col_1_data_Filter", 
    for_every_session_state="Col_1_for_every", 
    find_the_session_state="Col_1_find_the",
    of_session_state="Col_1_prices",
    chart_type_session_state="chart_type_column_1",
    load_session_state_col_2="column_2_submit",
    form_session_state_col_2="col_2_data_Filter", 
    for_every_session_state_col_2="Col_2_for_every", 
    find_the_session_state_col_2="Col_2_find_the",
    of_session_state_col_2="Col_2_prices",
    chart_type_session_state_2="chart_type_column_2",
    ):

    main_Cols = st.columns(2)

    with main_Cols[0]:
        
        if load_session_state not in st.session_state:
            st.session_state[load_session_state] = False

        def col_1_submit():
            st.session_state[load_session_state] = True

        with st.form(form_session_state):
            # cols = st.columns(3)
            # with cols[0]:
            data_to_select = data.columns.tolist()
            data_to_select.remove("currency")
            data_to_select.remove("prices of items on Amazon")
            st.selectbox(label="For every", options=data_to_select, key=for_every_session_state)
            # with cols[1]:
            st.multiselect(label="find the", options=['mean', 'median', 'max', 'min', "std", "quartile", "count"], key=find_the_session_state)
            # with cols[2]:
            st.selectbox(label="of", options=["prices of items on Amazon"], index=0, key=of_session_state)
            st.form_submit_button("Submit", on_click=col_1_submit)
        
        tabs1 = st.tabs(["Table", "Chart"])
        with tabs1[0]:

            if st.session_state[load_session_state] == False or st.session_state[for_every_session_state] == [] or st.session_state[find_the_session_state] == []:
                st.info("Fill in select boxes above to view table")
            
            else:
                if "quartile" in st.session_state[find_the_session_state]:
                    stat_measures = st.session_state[find_the_session_state]
                    stat_measures.remove("quartile")

                    df1 = data.groupby(st.session_state[for_every_session_state])[st.session_state[of_session_state]].agg(stat_measures)

                    def percentile(n):
                        def percentile_(x):
                            return np.percentile(x, n)
                        percentile_.__name__ = 'percentile_%s' % n
                        return percentile_
                    
                    df3 = data.groupby(st.session_state[for_every_session_state])[st.session_state[of_session_state]].agg([percentile(25), percentile(50), percentile(75)])
                    df = pd.concat([df1, df3], axis=1).dropna()
                else:
                    df = data.groupby(st.session_state[for_every_session_state])[st.session_state[of_session_state]].agg(st.session_state[find_the_session_state]).dropna()
                st.write(df, width=700)

        with tabs1[1]:
            if st.session_state[load_session_state] == False or st.session_state[for_every_session_state] == [] or st.session_state[find_the_session_state] == []:
                st.info("Please fill in select boxes to view chart")
                
            else:
                st.radio("Chart type", options=["line", "bar"] , horizontal=True, key=chart_type_session_state)
                if st.session_state[chart_type_session_state] == "line":
                    st.line_chart(df) 
                elif st.session_state[chart_type_session_state] == "bar":
                    st.bar_chart(df)
                #, x=st.session_state['Col_1_for_every'][0], y=st.session_state['Col_1_prices'])
    
    with main_Cols[1]:
        
        if load_session_state_col_2 not in st.session_state:
            st.session_state[load_session_state_col_2] = False

        def col_2_submit():
            st.session_state[load_session_state_col_2] = True

        with st.form(form_session_state_col_2):
            # cols = st.columns(3)
            # with cols[0]:
            data_to_select = data.columns.tolist()
            data_to_select.remove("currency")
            data_to_select.remove("prices of items on Amazon")
            st.selectbox(label="For every", options=data_to_select, key=for_every_session_state_col_2)
            # with cols[1]:
            st.multiselect(label="find the", options=['mean', 'median', 'max', 'min'], key=find_the_session_state_col_2)
            # with cols[2]:
            st.selectbox(label="of", options=["prices of items on Amazon"], index=0, key=of_session_state_col_2)
            st.form_submit_button("Submit", on_click=col_2_submit)
        
        tabs1 = st.tabs(["Table", "Chart"])
        with tabs1[0]:

            if st.session_state[load_session_state_col_2] == False or st.session_state[for_every_session_state_col_2] == [] or st.session_state[find_the_session_state_col_2] == []:
                st.info("Fill in select boxes above to view table")
            
            else:
                df = data.groupby(st.session_state[for_every_session_state_col_2])[st.session_state[of_session_state_col_2]].agg(st.session_state[find_the_session_state_col_2]).dropna()
                st.write(df, width=700)

        with tabs1[1]:
            if st.session_state[load_session_state_col_2] == False or st.session_state[for_every_session_state_col_2] == [] or st.session_state[find_the_session_state_col_2] == []:
                st.info("Please fill in select boxes to view chart")
                
            else:
                st.radio("Chart type", options=["line", "bar"] , horizontal=True, key=chart_type_session_state_2)
                if st.session_state[chart_type_session_state_2] == "line":
                    st.line_chart(df) 
                elif st.session_state[chart_type_session_state_2] == "bar":
                    st.bar_chart(df)
               
 
st.header("How price trends with other factors")
test()

# test(colNumber=1, load_session_state="column_2_submit", form_session_state="col_2_data_Filter", for_every_session_state="Col_2_for_every", 
#     find_the_session_state="Col_2_find_the", of_session_state="Col_2_prices")

st.write("")
st.write("")
st.write("")
st.write("")


test(
    # colNumber=0,
    load_session_state="column_3_submit",
    form_session_state="col_3_data_Filter", 
    for_every_session_state="Col_3_for_every", 
    find_the_session_state="Col_3_find_the",
    of_session_state="Col_3_prices",
    chart_type_session_state = "chart_type_column_3",
    load_session_state_col_2="column_4_submit",
    form_session_state_col_2="col_4_data_Filter", 
    for_every_session_state_col_2="Col_4_for_every", 
    find_the_session_state_col_2="Col_4_find_the",
    of_session_state_col_2="Col_4_prices",
    chart_type_session_state_2 = "chart_type_column_4"
    )


# st.header("Observe correlation between prices and other numerical factors") 
# scatter_cols = st.columns([5,4])

# with scatter_cols[0]:

#     data_Types = data.dtypes.to_frame()
#     data_Types_ = data_Types[(data_Types[0]== "float64") | (data_Types[0] == "int64")]
#     if "scatter_plot_load" not in st.session_state:
#             st.session_state["scatter_plot_load"] = False

#     def col_scatter_submit():
#         st.session_state["scatter_plot_load"] = True

#     with st.form("scatter_chart"):
#         st.selectbox("xAxis", options=data_Types_.index.tolist(), key="xAxis_")
#         st.selectbox("yAxis", options=data_Types_.index.tolist(), key="yAxis_")
#         st.form_submit_button("Submit", on_click=col_scatter_submit)

#     if st.session_state["scatter_plot_load"] == False or st.session_state['yAxis_'] == "" or st.session_state["xAxis_"] == "":
#         st.info("Please fill in the above to view the results")
#     else:
#         fig = px.scatter(data, x=st.session_state['xAxis_'], y=st.session_state['yAxis_'])
#         st.plotly_chart(fig, use_container_width=True)

    

# with scatter_cols[1]:
#     with st.form("Heatmap chart"):
#         st.selectbox("xAxis", options=["Hi"])
#         st.selectbox("yAxis", options=["hiya"])
#         st.form_submit_button("Submit")
