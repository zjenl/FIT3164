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



# #Reading the modified_price csv files
# df = pd.read_csv('modified_price.csv')
# #Transposing the csv files so that we can perform the data analysis
# df = df.transpose()
# #Changing the names of the columns
# df.columns = df.iloc[0,]

@st.experimental_fragment
def show_specific_products(data):
    time.sleep(1)

st.set_page_config(layout = 'wide')


st.title("FIT3164: Pricing Optimisation and Analysis")
st.header("Project Overview")
st.markdown("In the highly competitive world of retail, determining the proper price for products is a vital factor for manufacturers to ensure they are maximising their sales whilst also guaranteeing their profits. Pricing strategy is the core of a company's marketing strategy. The right pricing strategy not only has an impact on sales volume, but also plays a pivotal role in allowing companies to maximise profits, grow market share and further enhance their brand loyalty. There are multiple factors that can affect the pricing strategy of a product or service, including supply and demand of the products, pricing of competitors or whether the product itself is a necessity or not. ")
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

st.header("Team Member Introduction")
st.markdown("Working together as a group of four (Thanh Trung Tran, Zejinyi Liu, Shuen Y'ng Tan, Yun Gu), our group project aimed to explore the relative responsiveness of change in quantity demanded to different changes in unit price of multiple products,using  the datasets containing unit sales of different products of Walmart from Jan 2011 to April 2016. The objective is to recalibrate pricing strategies in resonance with market dynamics, thereby stimulating customer inclination to pay and enhancing overall company profitability. Thanh Trung Tran, the web developer and team leader, oversaw the project's direction and ensured seamless collaboration among team members. Zejinyi Liu, the data scientist and side project manager, focused on data analysis and modelling while also supporting project management tasks. Shuen Y'ng Tan, the project manager and side web developer, spearheaded the overall project management efforts and contributed to the web development aspects. Yun Gu, the admin and side data analyst, handled administrative tasks and supported data analysis activities alongside Zejinyi Liu.")

#Creating a text element to show we are reading the data
data_load_state = st.text('Loading data')
#Read the data
dataset = get_modified_price_data()
#Notify that the data was sucessfully loaded

st.subheader("Data analysis")
# st.line_chart(dataset)

# Create a selection of products without the duplicates
item = dataset['item_id'].drop_duplicates()
departments = dataset['dept_id'].drop_duplicates()

# Create the sidebar to select products from 

product_choice = st.sidebar.selectbox('Choose the item_id or department_id', item)
# departments_choice = st.sidebar.selectbox('Choose the department_id', departments)


##################################################################
#Filtering the dataset based on the input from the users.
st.header("Individual item price analysis")
st.markdown("On the left are select box where users can choose their specific item_id or choose to group by department_id in which they wish to observe the change in price elasticity model from. Upon choosing their wanted value, there will be 3 time series graph on the right, with the first one showcasing the change in price of either the individual items or average change in price of the products group by their respective department. The second graph will highlight the change in sales in a similar manner while the final graph will denote the change in elasticity of these products/departments over the span of 253 weeks from week 11101 to 11353 with the first week being labeled 11101 which starts counting from Saturday 29/01/2011")
# Select the rows containing the item_id of the selected item in the select box and manipulate the new rows to create a new data fram suitable to create a line graph to visualise
new_df = dataset.loc[dataset['item_id'] == product_choice]
new_df = new_df.transpose().replace(np.nan, 0)
new_df = new_df.drop(['item_id', 'dept_id'], axis = "index")
new_df.columns = ['Percent price change']
# new_df['Week'] = [str(x) for x in range(11101, 11354)]

st.line_chart(new_df)
#Display the dataframe in a line chart


# c = alt.Chart(new_df).mark_line().encode( x= "Week", y = 'Percent price change'
#                                           ).properties(title = 'Percent change in price over time for product {item_id}'.format(item_id = product_choice))


# st.altair_chart(c)
# st.markdown("Each of the line chart here display the change in price of each product in percentage in comparison to their previous week, with the first week being labeled 11101 which starts counting from Saturday 29/01/2011")

# new_df = dataset.loc[dataset['item_id'] == product_choice]
# new_df2 = new_df.transpose().replace(np.nan,0)
# a = len(new_df2.columns)
########################################################################
st.header("Individual item sales analysis")
st.markdown("In a similar manner, we manipulate the given datasets and aggregrate their sales based on each individual item_id and based on their respective department, and hence produce the graph showcase the change in sales of each product over their respective weeks")
dataset2 = get_modified_sales_data()
# Create a selection of products without the duplicates
# item2 = dataset2['item_id'].drop_duplicates()
# departments2 = dataset2['dept_id'].drop_duplicates()
# #Create new sidebar
# product_choice2 = st.sidebar.selectbox('Choose the item_id for sales change', item2)
# departments_choice2 = st.sidebar.selectbox('Choose the department_id for sales change', departments2)
new_df2 = dataset2.loc[dataset2['item_id'] == product_choice]
new_df3 = new_df2.transpose().replace(np.nan,0)
# new_df3 = new_df3[0]
#Dropping the item_id and dept_id row
new_df3 = new_df3.drop(['item_id', 'dept_id'], axis = "index")
new_df3 = new_df3.iloc[:, :1]
new_df3.columns = ['Sales']
new_df3['Week'] = [str(x) for x in range(11101, 11354)]


# st.line_chart(new_df3)
c1 = alt.Chart(new_df3).mark_line().encode( x= "Week", y = 'Sales'
                                          ).properties(title = 'Change in sales  over time for product {item_id}'.format(item_id = product_choice))


st.altair_chart(c1)

#Generating a linechart
# st.line_chart(new_df3)
# st.markdown("Each of the line chart here display the change in sales of each product in percentage in comparison to their previous week, with the first week being labeled 11101 which starts counting from Saturday 29/01/2011")
######################################################
st.header("Price Elasticity Modelling")
st.markdown("We originally explore our given Datsets to determine the percent change in price and sales of each products based on their product id, each is stored separately in a dataset. Afterwards, we calulate the price elasticity model of each product by divide the percent change in sales over the percent change in price and aim to observe if each products is either elastic or inelastic. However, upon examining each of the graphs produced, we can conclude that ")


#Reading the datasets
percent_sales = get_percent_change_sales()
percent_price = get_percent_change_price()

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
c2 = alt.Chart(price_elasticity_model).mark_line().encode( x= "Week", y = 'Elasticity'
                                          ).properties(title = 'Change in elasticity  over time for product {item_id}'.format(item_id = product_choice))

st.altair_chart(c2)

st.header("Additional Feature Engineering")
st.markdown("By implementing machine learning using the base RNN model, we are lookikng to predict the potential sales made when user get to choose their expected change in price (discount) and the model would product the expected sales")

number = st.number_input("Please enter the percent discount you want to apply to the product")
st.write("The current discount applied is {a}%".format(a = number))

# price_elasticity_model_ind = percent_price_ind2[]

# dataset.columns = dataset2.iloc[0,]
# dataset2 = dataset2.drop(['item_id', 'dept_id'], axis = "index")
# st.dataframe(dataset2)

# #Select the row with the user selected product_id
# new_df2 = dataset2[product_choice]
# #Create a new data frame
# st.dataframe(new_df2)
# #Display the dataframe in a line chart
# st.line_chart(new_df2)













