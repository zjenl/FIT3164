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
def get_percent_change_price(allow_output_mutation = True):
    df3 = pd.read_csv('percent_change_price.csv')
    return df3

@st.cache_data
def get_percent_change_sales(allow_output_mutation = True):
    df4 = pd.read_csv('percent_change_sale.csv')
    return df4


@st.cache_data
def get_modified_price_data(allow_output_mutation = True):
    df = pd.read_csv('modified_price.csv')
    df.head()
    # df = df.transpose()
    # df.columns = df.iloc[0,]
    # df = df.drop(['dept_id'], axis = 'index')
    # df = df.drop(['item_id', 'dept_id'], axis = "index")
    return df


st.header("Price Elasticity Modelling for individual products")
st.markdown("We originally explore our given Datsets to determine the percent change in price and sales of each products based on their product id, each is stored separately in a dataset. Afterwards, we calulate the price elasticity model of each product by divide the percent change in sales over the percent change in price and aim to observe if each products is either elastic or inelastic. Users can freely choose the item_id that they would like to observe their respective price elasticity modelling over time for")

dataset = get_modified_price_data()
#Reading the datasets
percent_sales = get_percent_change_sales()
percent_price = get_percent_change_price()

# Create a selection of products without the duplicates
item = dataset['item_id'].drop_duplicates()
item = item[0: len(item.index) -7, ]

# Create the sidebar to select products from 
product_choice = st.sidebar.selectbox('Choose the item_id', item)

## 
percent_sales_ind = percent_sales.loc[percent_sales['item_id'] == product_choice]
percent_sales_ind2 = percent_sales_ind.transpose().replace(np.nan, 0)
percent_sales_ind2 = percent_sales_ind2.drop(['item_id','dept_id'], axis = "index")



#Getting the 1st column of the dataset only
percent_sales_ind2 = percent_sales_ind2.iloc[:, :1]
percent_sales_ind2.columns = [product_choice]
percent_sales_ind2['Week'] = [str(x) for x in range(11101, 11354)]


percent_price_ind = percent_price.loc[percent_price['item_id'] == product_choice]
percent_price_ind2 = percent_price_ind.transpose().replace(np.nan, 0)
percent_price_ind2 = percent_price_ind2.drop(['item_id','dept_id'], axis = "index")
percent_price_ind2 = percent_price_ind2[:-1]
percent_price_ind2.columns = [product_choice]
for i in range(253-157):
    percent_price_ind2.loc[len(percent_price_ind2)-1] = [0]

percent_price_ind2['Week'] = [str(x) for x in range(11101, 11354)]
# percent_sales_ind2[product_choice] /= percent_sales_ind2['Week'].map(percent_price_ind2.set_index('Week')[product_choice]) 

percent_price_ind2.set_index('Week', inplace = True)
percent_sales_ind2.set_index('Week', inplace = True)

# st.dataframe(percent_price_ind2)
# st.dataframe(percent_sales_ind2)

price_elasticity_model = []
#Converting dataframe column to numpy Array
a = percent_sales_ind2[product_choice].values
b = percent_price_ind2[product_choice].values
#As there are 0 values in the dataset, hence we add an extra condition that will return 0 when dividing by zero
price_elasticity_model = np.divide(a, b, out = np.zeros_like(a), where =b != 0)

price_elasticity_model = pd.DataFrame(price_elasticity_model)
price_elasticity_model['Week'] = [str(x) for x in range(11101, 11354)]
price_elasticity_model.set_index('Week')
price_elasticity_model.columns = ['Elasticity', 'Week']

#Making the time series graph using alt.chart
c3 = alt.Chart(price_elasticity_model).mark_line().encode( x= "Week", y = 'Elasticity'
                                          ).properties(title = 'Change in elasticity  over time for product {item_id}'.format(item_id = product_choice))

st.altair_chart(c3)
