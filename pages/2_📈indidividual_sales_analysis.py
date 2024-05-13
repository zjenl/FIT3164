#Importing streamlit
import streamlit as st
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import pandas as pd
import time
import altair as alt


st.header("Individual item sales analysis")
st.markdown("In a similar manner, we manipulate the given datasets and aggregrate their sales based on each individual item_id and based on their respective department, and hence produce the graph showcase the change in sales of each product over their respective weeks")
@st.cache_data
def get_modified_sales_data(allow_output_mutation = True):
    df2 = pd.read_csv('modified_sales.csv')
    return df2

dataset2 = get_modified_sales_data()
# Create a selection of products without the duplicates
item = dataset2['item_id'].drop_duplicates()
item = item[0: len(item.index) -7, ]
#Getting the different store_id available
store = dataset2['store_id'].drop_duplicates()
store = store[0:10, ]

#Create a sidebar to select products from
product_choice = st.sidebar.selectbox('Choose the item_id or department_id', item)

#Create a sidebar to select store_id from
store_choice = st.sidebar.selectbox('Choose the store_id', store)

# Create a selection of products without the duplicates
# item2 = dataset2['item_id'].drop_duplicates()
# departments2 = dataset2['dept_id'].drop_duplicates()
# #Create new sidebar
# product_choice2 = st.sidebar.selectbox('Choose the item_id for sales change', item2)
# departments_choice2 = st.sidebar.selectbox('Choose the department_id for sales change', departments2)
new_df2 = dataset2.loc[(dataset2['item_id'] == product_choice) & (dataset2['store_id'] == store_choice)]
new_df3 = new_df2.transpose().replace(np.nan,0)



#Dropping the item_id and dept_id row
new_df3 = new_df3.drop(['item_id', 'dept_id', 'store_id'], axis = "index")
# Select the dataset of the given store
# new_df3 = new_df.loc['store_id']
# new_df3 = new_df3[0]

# new_df3 = new_df3.iloc[:, :1]
new_df3.columns = ['Sales']
new_df3['Week'] = [str(x) for x in range(11101, 11354)]


# st.line_chart(new_df3)
c1 = alt.Chart(new_df3).mark_line().encode( x= "Week", y = 'Sales'
                                          ).properties(title = 'Change in sales  over time for product {item_id} in store {store_id}'.format(item_id = product_choice, store_id = store_choice))


st.altair_chart(c1)
