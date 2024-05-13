#Importing streamlit
import streamlit as st
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import pandas as pd
import time
import altair as alt
from vega_datasets import data
import h5py 



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
@st.cache_data
def get_modified_sales_data(allow_output_mutation = True):
    df2 = pd.read_csv('modified_sales.csv')
    return df2
@st.cache_data
def get_percent_change_price(allow_output_mutation = True):
    df3 = pd.read_csv('percent_change_price.csv')
    return df3

@st.cache_data
def get_percent_change_sales(allow_output_mutation = True):
    df4 = pd.read_csv('percent_change_sale.csv')
    return df4




st.header("Price Elasticity Modelling aggregated by deparments")
st.markdown("After we conducted our price elasticity modelling for individual products, we notice that several products change of elasticity was rather not prominent and hard to detect, we decided to group all of their product sales and prices based on their department and then perform the price elasticity modelling on them instead. On the left, you can choose the departments that you wish to observe the price elasticity modelling for")

dataset2 = get_modified_sales_data()
#Reading the datasets
percent_sales = get_percent_change_sales()
percent_price = get_percent_change_price()


# Create a selection of departments without the duplicates
departments = dataset2['dept_id'].drop_duplicates()

# Create a sidebar to select departments from
department_choice = st.sidebar.selectbox('Choose the department_id', departments)

## 
percent_sales_ind = percent_sales.loc[percent_sales['item_id'] == department_choice]
percent_sales_ind2 = percent_sales_ind.transpose().replace(np.nan, 0)
percent_sales_ind2 = percent_sales_ind2.drop(['item_id','dept_id'], axis = "index")



#Getting the 1st column of the dataset only
percent_sales_ind2 = percent_sales_ind2.iloc[:, :1]
percent_sales_ind2.columns = [department_choice]
percent_sales_ind2['Week'] = [str(x) for x in range(11101, 11354)]


percent_price_ind = percent_price.loc[percent_price['item_id'] == department_choice]
percent_price_ind2 = percent_price_ind.transpose().replace(np.nan, 0)
percent_price_ind2 = percent_price_ind2.drop(['item_id','dept_id'], axis = "index")
percent_price_ind2 = percent_price_ind2[:-1]
percent_price_ind2.columns = [department_choice]
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
a = percent_sales_ind2[department_choice].values
b = percent_price_ind2[department_choice].values
#As there are 0 values in the dataset, hence we add an extra condition that will return 0 when dividing by zero
price_elasticity_model = np.divide(a, b, out = np.zeros_like(a), where =b != 0)

price_elasticity_model = pd.DataFrame(price_elasticity_model)
price_elasticity_model['Week'] = [str(x) for x in range(11101, 11354)]
price_elasticity_model.set_index('Week')
price_elasticity_model.columns = ['Elasticity', 'Week']

#Making the time series graph using alt.chart
c3 = alt.Chart(price_elasticity_model).mark_line().encode( x= "Week", y = 'Elasticity'
                                          ).properties(title = 'Change in elasticity  over time for items in department {dept_id}'.format(dept_id = department_choice))

st.altair_chart(c3)
