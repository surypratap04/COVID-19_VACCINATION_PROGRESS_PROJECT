import streamlit as st
import pandas as pd 

df = pd.read_excel('Employees_data.xlsx')

st.title('Analysis of Covid-19 Vaccination Progress')
st.markdown('![alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMxgsjlbZ2BNCv_OD_YrNAe3GNU6Bs79xtCg&usqp=CAU)')

st.dataframe(df) 

sidebar = st.sidebar

sidebar.header('Choose Your Action')

