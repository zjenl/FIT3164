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
def get_modified_sales_data(allow_output_mutation = True):
    df2 = pd.read_csv('modified_sales.csv')
    return df2

dataset2 = get_modified_sales_data()

# Create a selection of departments without the duplicates
departments = dataset2['dept_id'].drop_duplicates()

# Create a sidebar to select departments from
department_choice = st.sidebar.selectbox('Choose the department_id', departments)

# Department sales analysis
st.header("Department sales analysis")
st.markdown("Here we perform our data analysis on the sales aggregrated for each department, by choosing from the options of 10 stores across 3 particular states: Wiscosin (WI), Texas (TX), and  California (CA), you will be able to observe a line chart denoting their sales change aggregrated starting from week 11101 which starts on Saturady 29/01/2011.")
new_df4 = dataset2.loc[dataset2['item_id'] == department_choice]
new_df4 = new_df4.transpose().replace(np.nan,0)

#Dropping the item_id, dept_id and store_id row
new_df4 = new_df4.drop(['item_id', 'dept_id', 'store_id'], axis = "index")
new_df4.columns = ['Sales']
new_df4['Week'] = [str(x) for x in range(11101, 11354)]


#Constructing the line chart
c2 = alt.Chart(new_df4).mark_line().encode( x= "Week", y = 'Sales'
                                          ).properties(title = 'Change in sales  over time for department {dept_id}'.format(dept_id = department_choice))


st.altair_chart(c2)
