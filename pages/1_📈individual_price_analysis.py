#Importing streamlit
import streamlit as st
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import pandas as pd
import time
import altair as alt

@st.cache_data
def get_modified_price_data(allow_output_mutation = True):
    df = pd.read_csv('modified_price.csv')
    df.head()
    # df = df.transpose()
    # df.columns = df.iloc[0,]
    # df = df.drop(['dept_id'], axis = 'index')
    # df = df.drop(['item_id', 'dept_id'], axis = "index")
    return df


# departments_choice = st.sidebar.selectbox('Choose the department_id', departments)


##################################################################
#Filtering the dataset based on the input from the users.
dataset = get_modified_price_data()
st.header("Individual item price analysis")

# Create a selection of products without the duplicates
item = dataset['item_id'].drop_duplicates()
item = item[0: len(item.index) -7, ]

# Create the sidebar to select products from 
product_choice = st.sidebar.selectbox('Choose the item_id or department_id', item)

#############################
st.markdown("On the left are select box where users can choose their specific item_id or choose to group by department_id in which they wish to observe the change in price elasticity model from. Upon choosing their wanted value, there will be 3 time series graph on the right, with the first one showcasing the change in price of either the individual items or average change in price of the products group by their respective department. The second graph will highlight the change in sales in a similar manner while the final graph will denote the change in elasticity of these products/departments over the span of 253 weeks from week 11101 to 11353 with the first week being labeled 11101 which starts counting from Saturday 29/01/2011")
# Select the rows containing the item_id of the selected item in the select box and manipulate the new rows to create a new data fram suitable to create a line graph to visualise
new_df = dataset.loc[dataset['item_id'] == product_choice]
new_df = new_df.transpose().replace(np.nan, 0)
new_df = new_df.drop(['item_id', 'dept_id'], axis = "index")
new_df.columns = ['Percent price change']
# new_df['Week'] = [str(x) for x in range(11101, 11354)]
#Display the dataframe in a line chart
st.line_chart(new_df)