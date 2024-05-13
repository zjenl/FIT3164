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

st.header("Expected sales volume")
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

#Reading h5 file
food1 = h5py.File("FOODS_1_rnn_model.h5", 'r')

a = food1.keys()
st.write(a)

#Making 2 groups
group1 = food1['model_weights']
group2 = food1['optimizer_weights']

st.write(group1.keys())
st.write(group2.keys())
group3 = group1['top_level_model_weights']


st.write(group3.keys())
