import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu #navbar
st.set_page_config(layout="wide") #
st.title("Cric info app")
#loading Data
df=pd.read_csv("newfile.csv")

#---------NAVBAR------------#

select = option_menu(
    menu_title=None,
    options=["Home","Player Analysis","Country Insights","Comparison",
             "Data Explorer"],
    icons=["house","person","globe","bar-chart","table"],
    orientation="horizontal"

)


##-----------------Home--------------

if select == "Home":

    st.title("Cricket Analysis Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Players", df["Player"].nunique())

    col2.metric("Total Runs", df["Runs"].sum())

    col3.metric("Countries", df["Country"].nunique())

    st.dataframe(df.head())


#-----------Player Analysis----------------

elif select == "Player Analysis":

    st.title("Player Analysis")

    player = st.selectbox("Select Player", df["Player"])

    pdata = df[df["Player"]==player]
    pdata = pdata[["Matches", "innings", "Runs", "High_score", "Strike_rate", "100","50","6s","4s"]]
    transposeData = pdata.T.reset_index()

    st.dataframe(transposeData)


    fig = px.bar(
        transposeData,
        x= "index",
        y= transposeData.columns[1],
        color="index"
    )
    st.plotly_chart(fig, use_container_width=True)


#-----------Country------------


elif select == "Country Insights":
    st.title("Country Insights")

    country_runs = df.groupby("Country")["Runs"].sum().reset_index()
    fig= px.pie(country_runs,names="Country",values="Runs")
    st.plotly_chart(fig,use_container_width=True)

    country_select = st.selectbox("Select Country", df["Country"].unique())
    cData = df[df["Country"] == country_select]

    fig_runs = px.pie(
       cData,
       names="Player",
       values="Runs",
       color="Player" 
    )

    st.plotly_chart(fig_runs , use_container_width=True)


#-------------Comparison----------------



elif select== "Comparison":

    st.title("Player Comparison")

    players=st.multiselect(
        "Compare Players",
        df["Player"],
        default=df["Player"].head(5)
    )

    compare=df[df["Player"].isin(players)]

    fig=px.scatter(
        compare,
        x="Strike_rate",
        y="Ave",
        size="Runs",
        color="Country"

    )
    st.plotly_chart(fig,use_container_width=True)