#Importing streamlit
import streamlit as st
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from st_pages import hide_pages

st.title("FIT3164: Pricing Optimisation and Analysis")
st.header("Project Overview")
st.markdown("In the highly competitive world of retail, determining the proper price for products is a vital factor for manufacturers to ensure they are maximising their sales whilst also guaranteeing their profits. Pricing strategy is the core of a company's marketing strategy. The right pricing strategy not only has an impact on sales volume, but also plays a pivotal role in allowing companies to maximise profits, grow market share and further enhance their brand loyalty. There are multiple factors that can affect the pricing strategy of a product or service, including supply and demand of the products, pricing of competitors or whether the product itself is a necessity or not. ")


st.header("Team Member Introduction")
st.markdown("Working together as a group of four (Thanh Trung Tran, Zejinyi Liu, Shuen Y'ng Tan, Yun Gu), our group project aimed to explore the relative responsiveness of change in quantity demanded to different changes in unit price of multiple products,using  the datasets containing unit sales of different products of Walmart from Jan 2011 to April 2016. The objective is to recalibrate pricing strategies in resonance with market dynamics, thereby stimulating customer inclination to pay and enhancing overall company profitability. Thanh Trung Tran, the web developer and team leader, oversaw the project's direction and ensured seamless collaboration among team members. Zejinyi Liu, the data scientist and side project manager, focused on data analysis and modelling while also supporting project management tasks. Shuen Y'ng Tan, the project manager and side web developer, spearheaded the overall project management efforts and contributed to the web development aspects. Yun Gu, the admin and side data analyst, handled administrative tasks and supported data analysis activities alongside Zejinyi Liu.")

st.header("Dataset Introduction")
st.markdown("Something Something")



hide_pages(["login"])
#Adding a log out button
if st.button("Log out"):
    st.session_state["logged_in"] = False
    st.success("Logged out!")
    sleep(0.5)
    st.switch_page("app.py")