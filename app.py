import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_option_menu as stm

st.set_page_config(layout='wide')

st.title("Ecommerce Dashboard")

df = pd.read_excel("./newData.xlsx")

select = stm.option_menu(
    menu_title=None,
    options=["Home","Products","City"],
    icons=["house","cart","globe"],
    orientation="horizontal"
)


if select == "Home":

    st.header("Key Performance Indicator (KPI's)")
    col1, col2, col3, col4 ,col5= st.columns(5)
    col1.metric("Total Cities", df["City"].nunique())
    col2.metric("Total States", df["State"].nunique())
    col3.metric("Total Categories", df["Category"].nunique())
    col4.metric("Total Customers", df["Customer ID"].nunique())
    col5.metric("Total Sales", df["Sales"].sum().round(2))
   

    st.header("Business Charts")

    year_sales = df.groupby("Year")["Sales"].sum().sort_values().reset_index()

    fig_year = px.bar(
        year_sales,
        x="Year",
        y="Sales",
        color="Year",
        title="Sales by Years"
    )

    st.plotly_chart(fig_year, use_container_width=True)

    col1,col2 = st.columns(2)

    product_sales = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).reset_index().head()

    fig_product = px.pie(
       product_sales,
       names="Sub-Category", 
       values="Sales",
       color="Sub-Category",
       title="Most Sold Product"
    )

    city_sales = df.groupby("City")["Sales"].sum().sort_values(ascending=False).reset_index().head()

    fig_city = px.pie(
       city_sales,
       names="City", 
       values="Sales",
       color="City",
       title="Most Sales by Cities"
    )


    with col1:
        st.plotly_chart(fig_product, use_container_width=True)
    with col2:
        st.plotly_chart(fig_city, use_container_width=True)

    st.dataframe(df.head())


elif select == "Products":
    st.title("Product Analysis")

    products=st.multiselect(label="Select Products", options= df["Sub-Category"].unique(),default=df["Sub-Category"].unique())

    filteredProduct = df[df["Sub-Category"].isin(products)]

    sales = filteredProduct.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(
        sales,
        x= "Sub-Category",
        y="Sales",
        color="Sub-Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filteredProduct.head())

    
elif select == "City":
    st.title("City Analysis")

    products=st.multiselect(label="Select Products", options= df["City"].unique(),default=df["City"].unique())

    filteredProduct = df[df["City"].isin(products)]

    sales = filteredProduct.groupby("City")["Sales"].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(
        sales,
        x= "City",
        y="Sales",
        color="City"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filteredProduct.head())

    
